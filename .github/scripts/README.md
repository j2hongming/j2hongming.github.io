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

Security
- Treat your refresh tokens and client secrets as sensitive — store them in GitHub Secrets and do not print them in logs.
