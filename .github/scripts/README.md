Post memos to X (Twitter) — setup

This helper script posts new markdown list items from `source/memos/**` to X using the API v2 `/2/tweets` endpoint.

Secrets you should add to your repository (one of these options is required):

- OPTION A (easiest if you already have a user OAuth2 token):
  - `X_BEARER_TOKEN` — a user OAuth2 access token with the `tweet.write` scope.

- OPTION B (recommended for long-lived automation):
  - `X_CLIENT_ID` — your app's OAuth2 client id
  - `X_REFRESH_TOKEN` — a refresh token obtained for a user with `tweet.write` and `offline.access`
  - `X_CLIENT_SECRET` — optional, only if your app requires it (confidential client)

How it works
- The script will use `X_BEARER_TOKEN` if present.
- Otherwise it will try to refresh an access token using `X_CLIENT_ID` + `X_REFRESH_TOKEN` (and optional `X_CLIENT_SECRET`).
- If no valid token is available the Action runs in dry-run mode and prints found items instead of posting.

Notes & links
- To obtain an OAuth2 refresh token you must perform the OAuth2 Authorization Code flow for your app with `tweet.write` and `offline.access` scopes. See: https://developer.x.com/en/docs/auth/oauth2
- If your app receives 403 errors referencing insufficient access, follow the guidance at https://developer.x.com/en/portal/product to request the correct access level.

Using Tweepy
- The poster script now uses `tweepy` (if available) to post tweets via v2 (`Client.create_tweet`). The GitHub Action installs `tweepy` by default. If `tweepy` is not available the script falls back to a direct HTTP POST using `requests`.

Security
- Treat your refresh tokens and client secrets as sensitive — store them in GitHub Secrets and do not print them in logs.

Helper: obtain a refresh token (interactive)

If you don't have a refresh token, run the interactive helper included in this repo to perform the OAuth2 Authorization Code (PKCE) flow and capture a `refresh_token`:

```sh
python .github/scripts/get_refresh_token.py --client-id <CLIENT_ID> --redirect-uri http://localhost:8080/callback
```

- The helper will print the authorization URL; open it in a browser and authorize with scopes `tweet.write offline.access`.
- It runs a short-lived local server to capture the redirect and automatically exchanges the `code` for an `access_token` and `refresh_token`.
- Add the returned `refresh_token` to your GitHub Secrets as `X_REFRESH_TOKEN` and set `X_CLIENT_ID` (and `X_CLIENT_SECRET` if needed).

If you prefer manual steps, follow the OAuth2 Authorization Code flow described at https://developer.x.com/en/docs/auth/oauth2
