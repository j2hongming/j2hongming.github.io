#!/usr/bin/env python3
"""
Find newly added list items in memos files between the pushed commits and post them to X (Twitter) using OAuth1 (v1.1 API).

Behavior:
- Uses git diff between BEFORE and AFTER (from env) to find added lines that look like markdown list items ("- ...").
- For each added item, constructs a short status and POSTs to the v1.1 statuses/update.json endpoint using OAuth1.
- If API credentials are missing, it prints found items (dry run).

Set the following secrets in GitHub: X_API_KEY, X_API_SECRET_KEY, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
"""

import os
import re
import shlex
import subprocess
import sys
import time

import requests
from requests_oauthlib import OAuth1

# Configuration
BEFORE = os.environ.get('BEFORE')
AFTER = os.environ.get('AFTER')
REPO = os.environ.get('REPO', 'unknown/repo')
BRANCH_REF = os.environ.get('BRANCH', 'refs/heads/unknown')
FILES_GLOB = 'source/memos/'
POST_URL = 'https://api.twitter.com/1.1/statuses/update.json'
MAX_LEN = 280

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

# Prepare poster
X_KEY = os.environ.get('X_API_KEY')
X_KEY_SECRET = os.environ.get('X_API_SECRET_KEY')
X_TOKEN = os.environ.get('X_ACCESS_TOKEN')
X_TOKEN_SECRET = os.environ.get('X_ACCESS_TOKEN_SECRET')

is_dry_run = not (X_KEY and X_KEY_SECRET and X_TOKEN and X_TOKEN_SECRET)

# Build a repo file link to include in the status (optional)
branch_name = BRANCH_REF.replace('refs/heads/', '')
base_file_url = f'https://github.com/{REPO}/blob/{branch_name}/'

print(f'Found {len(added_items)} new item(s).')
for item in added_items:
    status = item
    # append short note / link if there is space
    suffix = f' — {REPO} (memos)'
    if len(status) + len(suffix) <= MAX_LEN:
        status = status + suffix
    else:
        # truncate and add ellipsis
        keep = MAX_LEN - len(suffix) - 3
        if keep > 0:
            status = status[:keep].rstrip() + '...' + suffix
        else:
            status = status[:MAX_LEN]

    if is_dry_run:
        print('Dry run: would post:', status)
        continue

    auth = OAuth1(X_KEY, X_KEY_SECRET, X_TOKEN, X_TOKEN_SECRET)
    try:
        resp = requests.post(POST_URL, auth=auth, data={'status': status}, timeout=15)
        if resp.status_code == 200:
            print('Posted:', status)
        else:
            print('Failed to post:', status)
            print('Status code:', resp.status_code, 'Body:', resp.text)
    except Exception as e:
        print('Exception while posting:', e)

    # small delay to be nice to the API
    time.sleep(1)

print('Done.')
