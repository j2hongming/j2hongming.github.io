#!/usr/bin/env python3
"""
Find newly added list items in memos files between the pushed commits and post them to X (Twitter) using API v2 with OAuth2.

Behavior:
- Uses git diff between BEFORE and AFTER (from env) to find added lines that look like markdown list items ("- ...").
- For each added item, constructs a short status and POSTs to the v2 endpoint `/2/tweets` using an OAuth2 access token.
- Supports obtaining an access token by refreshing a refresh token (recommended) or using a provided bearer token.
- If credentials are missing, it prints found items (dry run).

Required GitHub secrets (one of the following):
- `X_BEARER_TOKEN` (a user OAuth2 access token with `tweet.write`) OR
- `X_CLIENT_ID`, `X_REFRESH_TOKEN` (and optionally `X_CLIENT_SECRET`) + the app must have `tweet.write` and `offline.access`.

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

# Configuration
BEFORE = os.environ.get('BEFORE')
AFTER = os.environ.get('AFTER')
REPO = os.environ.get('REPO', 'unknown/repo')
BRANCH_REF = os.environ.get('BRANCH', 'refs/heads/unknown')
FILES_GLOB = 'source/memos/'
POST_URL = 'https://api.twitter.com/2/tweets'
MAX_LEN = 280

# OAuth2 secrets (from GitHub secrets)
X_BEARER_TOKEN = os.environ.get('X_BEARER_TOKEN')  # optional: direct user access token
X_CLIENT_ID = os.environ.get('X_CLIENT_ID')
X_CLIENT_SECRET = os.environ.get('X_CLIENT_SECRET')  # optional
X_REFRESH_TOKEN = os.environ.get('X_REFRESH_TOKEN')
# OAuth1 user-context secrets (API key/secret + user access token/secret)
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


# Decide how to obtain an access token or OAuth1 credentials
access_token = None
is_dry_run = False
use_oauth1 = False

# Detect OAuth1 user-context availability
if X_API_KEY and X_API_KEY_SECRET and X_ACCESS_TOKEN and X_ACCESS_TOKEN_SECRET:
    use_oauth1 = True
    print('OAuth1 credentials detected — will attempt to post using OAuth1 user context (API Key + Access Token).')
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
# Skip this check for OAuth1 (we will authenticate with OAuth1 user context directly)
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
    suffix = f' — {REPO} (memos)'
    if len(status) + len(suffix) <= MAX_LEN:
        status = status + suffix
    else:
        keep = MAX_LEN - len(suffix) - 3
        if keep > 0:
            status = status[:keep].rstrip() + '...' + suffix
        else:
            status = status[:MAX_LEN]

    if is_dry_run:
        print('Dry run: would post:', status)
        continue

    # Prefer using Tweepy for posting to v2 tweets endpoint
    try:
        import tweepy
    except Exception as e:
        print('Tweepy not available or failed to import:', e)
        print('Falling back to direct HTTP POST (requests).')
        try:
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            payload = {'text': status}
            resp = requests.post(POST_URL, headers=headers, json=payload, timeout=15)
            if resp.status_code in (200, 201):
                print('Posted (via requests):', status)
            else:
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text
                print('Failed to post (via requests):', status)
                print('Status code:', resp.status_code, 'Body:', body)
        except Exception as e:
            print('Exception while posting (requests fallback):', e)
        time.sleep(1)
        continue

    # Use Tweepy client with the user access token (provide client id/secret if available)
    try:
        # If OAuth1 credentials are available prefer that (API key/secret + access token/secret)
        if use_oauth1:
            client = tweepy.Client(
                consumer_key=X_API_KEY,
                consumer_secret=X_API_KEY_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET,
            )
        else:
            client_kwargs = {}
            # Supply OAuth2 client credentials if present (these may be optional)
            if X_CLIENT_ID:
                client_kwargs['consumer_key'] = X_CLIENT_ID
            if X_CLIENT_SECRET:
                client_kwargs['consumer_secret'] = X_CLIENT_SECRET
            client = tweepy.Client(access_token=access_token, **client_kwargs)

        resp = client.create_tweet(text=status)
        # Tweepy returns a Response with .data containing tweet id
        if resp and getattr(resp, 'data', None):
            print('Posted (via Tweepy):', status)
        else:
            print('Failed to post (via Tweepy):', status, 'Response:', resp)
    except Exception as e:
        err_str = str(e)
        print('Exception while posting (via Tweepy):', e)
        # Provide a helpful hint for common error where Tweepy expects consumer key/secret
        if 'consumer' in err_str.lower() or 'consumer key' in err_str.lower() or 'consumer_key' in err_str.lower():
            print('It looks like Tweepy attempted to use OAuth1 internals but no consumer key/secret were provided.')
            print('If you have a client id/secret for your app, set `X_CLIENT_ID` and `X_CLIENT_SECRET` in repository secrets.')
            print('Falling back to direct HTTP POST using the access token (may still fail if token is app-only).')
        # Fallback to direct HTTP POST
        try:
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            payload = {'text': status}
            resp = requests.post(POST_URL, headers=headers, json=payload, timeout=15)
            if resp.status_code in (200, 201):
                print('Posted (via requests fallback):', status)
            else:
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text
                print('Failed to post (via requests fallback):', status)
                print('Status code:', resp.status_code, 'Body:', body)
        except Exception as e2:
            print('Exception while posting (requests fallback):', e2)

    # polite delay
    time.sleep(1)

print('Done.')
