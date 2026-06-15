#!/usr/bin/env python3
"""One-time YouTube OAuth: turn CLIENT_ID/SECRET into a long-lived REFRESH_TOKEN.

LOCAL ONLY. Run on the machine that will upload, signed in to the *channel owner's*
Google account in the default browser. It opens a consent page, the owner clicks
"Allow", the auth code is captured on a localhost loopback, exchanged for a refresh
token, and YOUTUBE_REFRESH_TOKEN is written into the local .env (which is gitignored).

Secrets never leave this machine and the refresh token is never printed in full
(rule 03). Cloud Claude cannot run this — it needs the owner's browser/account.

Owner prerequisites (Google Cloud Console, one time):
  1. Create/select a project; APIs & Services -> enable "YouTube Data API v3".
  2. OAuth consent screen: User type External; add your Google account as a Test user.
  3. Credentials -> Create credentials -> OAuth client ID -> Application type: Desktop app.
  4. Put the values into .env:  YOUTUBE_CLIENT_ID=...   YOUTUBE_CLIENT_SECRET=...

Then run:  python scripts/youtube_auth.py
"""
from __future__ import annotations

import http.server
import json
import secrets
import socket
import urllib.parse
import urllib.request
from pathlib import Path

SCOPES = (
    "https://www.googleapis.com/auth/youtube.upload "
    "https://www.googleapis.com/auth/youtube.readonly"
)
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def _read_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def _write_refresh_token(token: str) -> None:
    """Upsert YOUTUBE_REFRESH_TOKEN in .env without touching other lines."""
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    out, found = [], False
    for line in lines:
        if line.strip().startswith("YOUTUBE_REFRESH_TOKEN="):
            out.append(f"YOUTUBE_REFRESH_TOKEN={token}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"YOUTUBE_REFRESH_TOKEN={token}")
    ENV_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> int:
    env = _read_env()
    client_id = env.get("YOUTUBE_CLIENT_ID")
    client_secret = env.get("YOUTUBE_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("ERROR: set YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in .env first "
              "(see this script's header for the Google Cloud steps).")
        return 2

    port = _free_port()
    redirect_uri = f"http://127.0.0.1:{port}/"
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",      # required for a refresh token
        "prompt": "consent",           # force a refresh token even on re-auth
        "state": state,
    }
    auth_link = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    captured: dict[str, str] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            captured["code"] = (q.get("code") or [""])[0]
            captured["state"] = (q.get("state") or [""])[0]
            captured["error"] = (q.get("error") or [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<h2>Authorization received.</h2>"
                b"<p>You can close this tab and return to the terminal.</p>"
            )

        def log_message(self, *a):  # keep the terminal clean
            return

    print("\nOpen this URL in the browser signed in to the channel owner's Google account,")
    print("then click Allow:\n")
    print(auth_link + "\n")
    try:
        import webbrowser
        webbrowser.open(auth_link)
    except Exception:
        pass

    httpd = http.server.HTTPServer(("127.0.0.1", port), Handler)
    httpd.handle_request()  # serve exactly one redirect
    httpd.server_close()

    if captured.get("error"):
        print(f"ERROR: authorization denied/failed: {captured['error']}")
        return 1
    if not captured.get("code") or captured.get("state") != state:
        print("ERROR: no code returned or state mismatch (possible CSRF). Aborting.")
        return 1

    data = urllib.parse.urlencode({
        "code": captured["code"],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())

    refresh = body.get("refresh_token")
    if not refresh:
        print("ERROR: no refresh_token in response. Re-run after revoking prior access, "
              "and ensure prompt=consent + access_type=offline (this script sets both).")
        return 1

    _write_refresh_token(refresh)
    # Never print the token itself (rule 03 — no secrets in logs).
    print(f"\nOK: YOUTUBE_REFRESH_TOKEN written to {ENV_PATH} (gitignored). "
          "Do not commit .env. Verify with the provider auth_check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
