#!/bin/bash
# Local testing script for post_memos_to_x.py
# Usage: bash .github/scripts/test_local.sh

set -e

echo "=== Local Test for Post Memos to X ==="
echo ""

# Check Python and dependencies
python3 --version
echo "Checking dependencies..."
python3 -m pip install -q requests tweepy || {
  echo "Failed to install dependencies"
  exit 1
}
echo "✓ Dependencies installed"
echo ""

# Get recent commits for testing
REPO_ROOT=$(git rev-parse --show-toplevel)
BEFORE=$(git rev-parse HEAD~1 2>/dev/null || git rev-parse HEAD)
AFTER=$(git rev-parse HEAD)

echo "=== Test Configuration ==="
echo "BEFORE commit: $BEFORE"
echo "AFTER commit:  $AFTER"
echo ""

# Check for OAuth2 credentials
if [ -z "$X_CLIENT_ID" ] || [ -z "$X_REFRESH_TOKEN" ]; then
  echo "⚠️  Missing OAuth2 credentials!"
  echo ""
  echo "Please set these environment variables before running:"
  echo "  export X_CLIENT_ID='your-client-id'"
  echo "  export X_CLIENT_SECRET='your-client-secret'  # optional for PKCE"
  echo "  export X_REFRESH_TOKEN='your-refresh-token'"
  echo ""
  echo "Then run this script again:"
  echo "  bash .github/scripts/test_local.sh"
  exit 0
fi

echo "✓ OAuth2 credentials detected"
echo ""

# Run the script in dry-run or post mode
echo "=== Running Script ==="
cd "$REPO_ROOT"
export BEFORE="$BEFORE"
export AFTER="$AFTER"
export REPO=$(git config --get remote.origin.url | sed 's/.*[:/]\([^/]*\)\/\([^/]*\)\.git$/\1\/\2/')
export BRANCH="refs/heads/$(git rev-parse --abbrev-ref HEAD)"

echo "Env vars set:"
echo "  BEFORE=$BEFORE"
echo "  AFTER=$AFTER"
echo "  REPO=$REPO"
echo "  BRANCH=$BRANCH"
echo ""

python3 .github/scripts/post_memos_to_x.py
