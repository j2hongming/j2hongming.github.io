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


# Decide how to obtain an access token
access_token = None
is_dry_run = False

if X_BEARER_TOKEN:
    access_token = X_BEARER_TOKEN
elif X_CLIENT_ID and X_REFRESH_TOKEN:
    print('Refreshing access token using refresh token...')
    access_token = refresh_access_token(X_CLIENT_ID, X_REFRESH_TOKEN, X_CLIENT_SECRET)
    if not access_token:
        print('Token refresh failed: will run in dry-run mode and print found items.')
        is_dry_run = True
else:
    print('No bearer token nor refresh config found: running in dry-run mode and printing items.')
    is_dry_run = True

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

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    payload = {'text': status}
    try:
        resp = requests.post(POST_URL, headers=headers, json=payload, timeout=15)
    except Exception as e:
        print('Exception while posting:', e)
        continue

    if resp.status_code in (200, 201):
        print('Posted:', status)
    else:
        # Handle known error codes
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        print('Failed to post:', status)
        print('Status code:', resp.status_code, 'Body:', body)
        # Helpful guidance for common permission error
        if resp.status_code == 403:
            print("Permission error (403). Your app might not have the required `tweet.write` scope or access level.")
            print('See https://developer.x.com/en/portal/product and ensure your app has `tweet.write` and `offline.access` if using refresh tokens.')

    # polite delay
    time.sleep(1)

print('Done.')
