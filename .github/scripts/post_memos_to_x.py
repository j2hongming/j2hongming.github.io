#!/usr/bin/env python3
"""
Find newly added list items in memos files between the pushed commits and post them to X (Twitter) using API v2 with OAuth2.

Behavior:
- Uses git diff between BEFORE and AFTER (from env) to find added lines that look like markdown list items ("- ...").
- For each added item, constructs a short status and POSTs to the v2 endpoint `/2/tweets` using an OAuth2 access token.
- Supports obtaining an access token by refreshing a refresh token (recommended) or using a provided bearer token.
- If credentials are missing, it prints found items (dry run).

GitHub Actions setup (recommended):
1. Obtain OAuth2 credentials with refresh token:
   - X_CLIENT_ID: Your Twitter App's Client ID
   - X_CLIENT_SECRET: Your Twitter App's Client Secret (optional for PKCE flow)
   - X_REFRESH_TOKEN: A refresh token with scopes `tweet.write offline.access`
   
2. Add these as GitHub repository secrets

Alternative: OAuth1 user context
- X_API_KEY: Your Twitter App API Key
- X_API_KEY_SECRET: Your Twitter App API Key Secret
- X_ACCESS_TOKEN: The user access token
- X_ACCESS_TOKEN_SECRET: The user access token secret

Alternative (direct bearer token):
- X_BEARER_TOKEN: A user OAuth2 access token with `tweet.write` scope
  (Note: Bearer tokens expire and must be manually refreshed, so refresh token flow is recommended)

See `.github/scripts/README.md` for setup guidance.
"""

import os
import re
import shlex
import subprocess
import sys
import time
from typing import Optional

import requests
from requests_oauthlib import OAuth1Session

# Configuration
BEFORE = os.environ.get('BEFORE')
AFTER = os.environ.get('AFTER')
REPO = os.environ.get('REPO', 'unknown/repo')
BRANCH_REF = os.environ.get('BRANCH', 'refs/heads/unknown')
FILES_GLOB = 'source/memos/'
POST_URL = 'https://api.twitter.com/2/tweets'
MAX_LEN = 280
# Retry config for transient errors (e.g., 503 Service Unavailable)
MAX_RETRIES = 5
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
BACKOFF_BASE = 1.0  # seconds

# OAuth2 secrets (from GitHub secrets)
X_BEARER_TOKEN = os.environ.get('X_BEARER_TOKEN')  # optional: direct user access token
X_CLIENT_ID = os.environ.get('X_CLIENT_ID')
X_CLIENT_SECRET = os.environ.get('X_CLIENT_SECRET')  # optional
X_REFRESH_TOKEN = os.environ.get('X_REFRESH_TOKEN')
# OAuth1 user-context secrets (from GitHub secrets)
X_API_KEY = os.environ.get('X_API_KEY')
X_API_KEY_SECRET = os.environ.get('X_API_KEY_SECRET')
X_ACCESS_TOKEN = os.environ.get('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.environ.get('X_ACCESS_TOKEN_SECRET')

if not BEFORE or not AFTER:
    print('Missing BEFORE or AFTER commit; exiting.')
    sys.exit(0)

# Get diff
cmd = ['git', 'diff', '--no-color', '--unified=0', f'{BEFORE}', f'{AFTER}', '--', FILES_GLOB]
print('Running:', ' '.join(shlex.quote(p) for p in cmd))
proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if proc.returncode != 0:
    print('git diff failed:', proc.stderr)
    sys.exit(1)

diff = proc.stdout.splitlines()

# Parse added lines that are markdown list items
added_items = []
pattern = re.compile(r'^\+\s*-\s*(.*)')
for line in diff:
    m = pattern.match(line)
    if m:
        text = m.group(1).strip()
        if text:
            added_items.append(text)

if not added_items:
    print('No new memo list items found in this push.')
    sys.exit(0)

print(f'Found {len(added_items)} new item(s).')


def refresh_access_token(client_id: str, refresh_token: str, client_secret: Optional[str] = None) -> Optional[str]:
    """Obtain a new access token using the OAuth2 refresh token flow.
    Returns the access token string on success, or None on failure.
    """
    token_url = 'https://api.twitter.com/2/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }

    # If client_secret is not provided (PKCE clients), include client_id in body.
    if client_secret:
        # Use HTTP Basic auth with client_id:client_secret
        auth = (client_id, client_secret)
    else:
        auth = None
        data['client_id'] = client_id

    try:
        resp = requests.post(token_url, headers=headers, data=data, auth=auth, timeout=15)
    except Exception as e:
        print('Exception while refreshing token:', e)
        return None

    if resp.status_code != 200:
        print('Failed to refresh access token. Status code:', resp.status_code, 'Body:', resp.text)
        return None

    j = resp.json()
    access_token = j.get('access_token')
    if not access_token:
        print('No access_token in token response:', j)
        return None

    return access_token


# Decide how to authenticate
access_token = None
is_dry_run = False
use_oauth1 = False

# Prefer OAuth1 user context if full credentials are available
if X_API_KEY and X_API_KEY_SECRET and X_ACCESS_TOKEN and X_ACCESS_TOKEN_SECRET:
    use_oauth1 = True
    print('OAuth1 credentials detected — will attempt to post using OAuth1 user context.')
else:
    # Prefer a direct bearer (user) token if provided
    if X_BEARER_TOKEN:
        access_token = X_BEARER_TOKEN
    elif X_CLIENT_ID and X_REFRESH_TOKEN:
        print('Refreshing access token using refresh token...')
        access_token = refresh_access_token(X_CLIENT_ID, X_REFRESH_TOKEN, X_CLIENT_SECRET)
        if not access_token:
            print('Token refresh failed: will run in dry-run mode and print found items.')
            is_dry_run = True
    else:
        print('No bearer token, refresh config, or OAuth1 credentials found: running in dry-run mode and printing items.')
        is_dry_run = True

# Token-type check (verify this is a user-context token)
if not is_dry_run and not use_oauth1:
    print('Verifying token is user-context by calling GET /2/users/me')
    try:
        me_resp = requests.get('https://api.twitter.com/2/users/me', headers={'Authorization': f'Bearer {access_token}'}, timeout=10)
    except Exception as e:
        print('Exception while checking token type:', e)
        print('Proceeding in dry-run mode.')
        is_dry_run = True
        me_resp = None

    if me_resp is not None and me_resp.status_code != 200:
        # Handle unsupported/authentication errors and guidance
        try:
            me_body = me_resp.json()
        except Exception:
            me_body = me_resp.text
        print('GET /2/users/me returned', me_resp.status_code, me_body)
        if me_resp.status_code == 403 and isinstance(me_body, dict) and me_body.get('type', '').endswith('unsupported-authentication'):
            print('\nUnsupported Authentication (403): the token appears to be an application-only token (app context).')
            print('Posting requires a user-context token (OAuth 1.0a user context or OAuth2 user context).')
            print('Remediation: obtain a user refresh token via the OAuth2 Authorization Code flow (scopes: `tweet.write offline.access`) and set `X_REFRESH_TOKEN` and `X_CLIENT_ID` in repository secrets.')
            print('See .github/scripts/README.md for a helper to perform the one-time authorization.')
            is_dry_run = True
        elif me_resp.status_code == 401:
            print('\nUnauthorized (401): token is invalid or expired. Try refreshing or obtaining a user token.')
            is_dry_run = True
        else:
            # Other non-200 — fail-safe to dry-run
            print('\nUnexpected response from /2/users/me: running in dry-run mode to avoid accidental posts.')
            is_dry_run = True
    elif me_resp is not None and me_resp.status_code == 200:
        try:
            me = me_resp.json()
            user = me.get('data', {})
            print('Token verified for user:', user.get('username') or user.get('id'))
        except Exception:
            print('Token verified (could not parse user info).')

# Prepare and post items
for item in added_items:
    status = item
    # trim to MAX_LEN if necessary, adding an ellipsis when we cut
    if len(status) > MAX_LEN:
        status = status[:MAX_LEN-3].rstrip() + '...'

    if is_dry_run:
        print('Dry run: would post:', status)
        continue

    # Helper: post via requests with retries
    def post_requests_with_retries(text: str) -> bool:
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        payload = {'text': text}
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.post(POST_URL, headers=headers, json=payload, timeout=15)
            except Exception as e:
                print(f'Exception while posting (requests) attempt {attempt}:', e)
                resp = None

            status_code = getattr(resp, 'status_code', None)
            if resp is not None and status_code in (200, 201):
                print('Posted (via requests):', text)
                return True

            # Extract body for logging
            body = None
            if resp is not None:
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text

            # If status is retryable, wait and retry
            if status_code in RETRYABLE_STATUS or resp is None:
                wait = min(60, BACKOFF_BASE * (2 ** (attempt - 1)))
                print(f'Retryable response (attempt {attempt}) status={status_code} body={body}; retrying after {wait}s')
                time.sleep(wait)
                continue

            # Non-retryable failure
            print('Failed to post (via requests):', text)
            print('Status code:', status_code, 'Body:', body)
            return False

        print('Exceeded max retries for requests POST; giving up on:', text)
        return False

    # Helper: post via OAuth1 with retries
    def post_oauth1_with_retries(text: str) -> bool:
        payload = {'text': text}
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                oauth = OAuth1Session(
                    client_key=X_API_KEY,
                    client_secret=X_API_KEY_SECRET,
                    resource_owner_key=X_ACCESS_TOKEN,
                    resource_owner_secret=X_ACCESS_TOKEN_SECRET,
                )
                resp = oauth.post(POST_URL, json=payload, timeout=15)
            except Exception as e:
                print(f'Exception while posting (via OAuth1) attempt {attempt}:', e)
                resp = None

            status_code = getattr(resp, 'status_code', None)
            if resp is not None and status_code in (200, 201):
                print('Posted (via OAuth1):', text)
                return True

            body = None
            if resp is not None:
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text

            if status_code in RETRYABLE_STATUS or resp is None:
                wait = min(60, BACKOFF_BASE * (2 ** (attempt - 1)))
                print(f'Retryable response (attempt {attempt}) status={status_code} body={body}; retrying after {wait}s')
                time.sleep(wait)
                continue

            print('Failed to post (via OAuth1):', text)
            print('Status code:', status_code, 'Body:', body)
            return False

        print('Exceeded max retries for OAuth1 POST; giving up on:', text)
        return False

    # Helper: post via Tweepy with retries
    def post_tweepy_with_retries(text: str) -> bool:
        try:
            import tweepy
        except Exception as e:
            print('Tweepy not available or failed to import:', e)
            return post_requests_with_retries(text)

        # Build client
        try:
            client_kwargs = {}
            if X_CLIENT_ID:
                client_kwargs['consumer_key'] = X_CLIENT_ID
            if X_CLIENT_SECRET:
                client_kwargs['consumer_secret'] = X_CLIENT_SECRET
            client = tweepy.Client(access_token=access_token, **client_kwargs)
        except Exception as e:
            print('Exception while constructing Tweepy client:', e)
            return post_requests_with_retries(text)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = client.create_tweet(text=text)
            except Exception as e:
                err_str = str(e)
                # Try to detect transient 5xx in the exception text
                if any(code in err_str for code in ('503', '502', '504', '500', '429')):
                    wait = min(60, BACKOFF_BASE * (2 ** (attempt - 1)))
                    print(f'Exception while posting (via Tweepy) attempt {attempt}:', e)
                    print(f'Retrying after {wait}s')
                    time.sleep(wait)
                    continue
                print('Exception while posting (via Tweepy):', e)
                return post_requests_with_retries(text)

            # If Tweepy returns a response object, check for data
            if resp and getattr(resp, 'data', None):
                print('Posted (via Tweepy):', text)
                return True

            # Inspect resp for status info if possible
            status_code = None
            try:
                # Tweepy Response may have .status or underlying http response
                status_code = getattr(resp, 'status', None) or None
            except Exception:
                status_code = None

            if status_code in RETRYABLE_STATUS:
                wait = min(60, BACKOFF_BASE * (2 ** (attempt - 1)))
                print(f'Tweepy returned retryable status {status_code}; retrying after {wait}s')
                time.sleep(wait)
                continue

            # Non-retryable or unknown failure — fall back to requests
            print('Failed to post (via Tweepy):', text, 'Response:', resp)
            return post_requests_with_retries(text)

    if use_oauth1:
        posted = post_oauth1_with_retries(status)
    else:
        # Post using Tweepy (OAuth2)
        posted = post_tweepy_with_retries(status)
    if not posted:
        print('Giving up on posting item after retries:', status)

    # polite delay between items
    time.sleep(1)

print('Done.')
