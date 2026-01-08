import os
import base64
import hashlib
import re
import requests
from flask import Flask, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session storage

# --- CONFIGURATION (Can be provided via CLI args or environment variables) ---
# Set via CLI: --client-id / --client-secret, or environment variables CLIENT_ID / CLIENT_SECRET
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://127.0.0.1:8080/callback")

# --- HELPERS ---
def create_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

# --- ROUTES ---

@app.route("/")
def index():
    return '<a href="/login">Connect to X (Twitter)</a>'

@app.route("/login")
def login():
    code_verifier, code_challenge = create_pkce_challenge()
    
    # Store verifier in session to use later in the callback
    session["code_verifier"] = code_verifier
    
    scopes = "tweet.read tweet.write users.read offline.access"
    state = "state123" 
    
    auth_url = (
        f"https://twitter.com/i/oauth2/authorize?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={scopes}&state={state}"
        f"&code_challenge={code_challenge}&code_challenge_method=S256"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    code_verifier = session.get("code_verifier")
    
    token_url = "https://api.x.com/2/oauth2/token"
    
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    }
    
    # Exchange code for tokens
    if CLIENT_SECRET:
        response = requests.post(token_url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    else:
        # Public (PKCE) client - include client_id in body
        data["client_id"] = CLIENT_ID
        response = requests.post(token_url, data=data)
    tokens = response.json()

    print("Obtained tokens:", tokens)
    
    # In a real app, save these to a database!
    session["access_token"] = tokens.get("access_token")
    session["refresh_token"] = tokens.get("refresh_token")
    
    return "Authenticated! You can now <a href='/post_tweet'>Post a Tweet</a> or <a href='/refresh'>Refresh Token</a>."

@app.route("/post_tweet")
def post_tweet():
    access_token = session.get("access_token")
    if not access_token:
        return redirect("/login")

    url = "https://api.x.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"text": "Testing OAuth 2.0 with Flask! 🤖"}
    
    res = requests.post(url, json=payload, headers=headers)
    return jsonify(res.json())

@app.route("/refresh")
def refresh():
    old_refresh_token = session.get("refresh_token")
    if not old_refresh_token:
        return "No refresh token found."

    token_url = "https://api.x.com/2/oauth2/token"
    data = {
        "refresh_token": old_refresh_token,
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
    }
    
    if CLIENT_SECRET:
        response = requests.post(token_url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    else:
        response = requests.post(token_url, data=data)
    new_tokens = response.json()
    
    # IMPORTANT: Update session/DB with the NEW refresh token
    session["access_token"] = new_tokens.get("access_token")
    session["refresh_token"] = new_tokens.get("refresh_token")
    
    return "Token Refreshed! <a href='/post_tweet'>Post a Tweet</a>"

if __name__ == "__main__":
    import argparse
    import getpass

    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", help="OAuth Client ID")
    parser.add_argument("--client-secret", help="OAuth Client Secret (optional)")
    parser.add_argument("--redirect-uri", default=os.environ.get("REDIRECT_URI", "http://127.0.0.1:8080/callback"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    # Prefer CLI args, then environment variables, then prompt
    if args.client_id:
        CLIENT_ID = args.client_id
    if args.client_secret:
        CLIENT_SECRET = args.client_secret

    if not CLIENT_ID:
        CLIENT_ID = input("Enter CLIENT_ID: ").strip()

    if CLIENT_SECRET is None:
        try:
            s = getpass.getpass("Enter CLIENT_SECRET (leave blank if public client): ")
            CLIENT_SECRET = s if s != "" else None
        except Exception:
            CLIENT_SECRET = input("Enter CLIENT_SECRET (leave blank if public client): ").strip() or None

    REDIRECT_URI = args.redirect_uri

    if not CLIENT_ID:
        print("CLIENT_ID is required. Provide via --client-id or CLIENT_ID env var.")
        exit(1)

    app.run(host=args.host, port=args.port)
