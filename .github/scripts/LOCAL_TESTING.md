# Local Testing Guide for post_memos_to_x.py

## Quick Start

### 1. Install Dependencies
```bash
pip install requests tweepy
```

### 2. Set OAuth2 Credentials
Create a `.env.local` file or set environment variables:

```bash
export X_CLIENT_ID="your_client_id_here"
export X_CLIENT_SECRET="your_client_secret_here"  # optional for PKCE flow
export X_REFRESH_TOKEN="your_refresh_token_here"
```

To get these credentials:
1. Create a Twitter/X app at https://developer.twitter.com/
2. Set OAuth 2.0 scopes to: `tweet.write offline.access`
3. Get the Client ID, Client Secret (if applicable)
4. Obtain a refresh token using the OAuth2 Authorization Code flow

### 3. Test with Recent Commits

Option A - Using the test script:
```bash
bash .github/scripts/test_local.sh
```

Option B - Manual test with your commits:

Get two commits to test with (must have changes in `source/memos/`):
```bash
# Use specific commits
export BEFORE="commit_hash_1"
export AFTER="commit_hash_2"

# Or use HEAD~1 and HEAD
export BEFORE=$(git rev-parse HEAD~1)
export AFTER=$(git rev-parse HEAD)
```

Then run:
```bash
export REPO="your-github-username/your-repo"
export BRANCH="refs/heads/main"
python3 .github/scripts/post_memos_to_x.py
```

## Expected Behavior

### Dry-Run Mode (No Credentials)
If credentials are missing, the script will print found items without posting:
```
No bearer token or refresh config found: running in dry-run mode and printing items.
Dry run: would post: <your memo item>
```

### Successful Run (With Credentials)
```
Found <N> new item(s).
Refreshing access token using refresh token...
Token verified for user: @your_username
Verifying token is user-context by calling GET /2/users/me
Posted (via Tweepy): <memo text>
Done.
```

## Testing without Real OAuth2 Credentials

If you don't have Twitter/X OAuth2 credentials yet, you can test the script logic:

```bash
# Create test memos (must be in source/memos/)
mkdir -p source/memos
echo "- Test memo item 1" >> source/memos/2026-04-09.md
git add source/memos/
git commit -m "Add test memo"

# Run in dry-run mode (no credentials needed)
export BEFORE=$(git rev-parse HEAD~1)
export AFTER=$(git rev-parse HEAD)
export REPO="test/repo"
export BRANCH="refs/heads/main"
python3 .github/scripts/post_memos_to_x.py
```

This will show what would be posted without actually posting to Twitter/X.

## Troubleshooting

**ModuleNotFoundError: No module named 'tweepy'**
- Run: `pip install tweepy requests`

**import requests_oauthlib** error
- This module is no longer needed (OAuth1 support removed)
- Just install: `pip install requests tweepy`

**Token refresh failed**
- Check your `X_CLIENT_ID`, `X_CLIENT_SECRET`, and `X_REFRESH_TOKEN` are correct
- Refresh tokens expire after 6 months of inactivity

**403 Unsupported Authentication error**
- Your credentials may be for app-only auth (not user context)
- You need a user-context token obtained via OAuth2 Authorization Code flow
- See Twitter Developer documentation for authorization

## Next Steps

Once testing locally works perfectly:
1. Add `X_CLIENT_ID`, `X_CLIENT_SECRET`, and `X_REFRESH_TOKEN` as GitHub repository secrets
2. Commit and push changes
3. Create/update a memo file in `source/memos/` and push
4. GitHub Actions will automatically post it for you!
