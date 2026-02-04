import requests
from config import OKAPI_BASE_URL, OKAPI_TENANT, OKAPI_USERNAME, OKAPI_PASSWORD

LOGIN_PATH = "/authn/login-with-expiry"


class FolioAuthError(Exception):
    pass


def get_okapi_token() -> str:
    """
    Logs into FOLIO and returns an Okapi access token.
    """
    if not (OKAPI_BASE_URL and OKAPI_TENANT and OKAPI_USERNAME and OKAPI_PASSWORD):
        raise FolioAuthError("Missing OKAPI configuration (check your .env).")

    url = f"{OKAPI_BASE_URL}{LOGIN_PATH}"
    headers = {
        "x-okapi-tenant": OKAPI_TENANT,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"username": OKAPI_USERNAME, "password": OKAPI_PASSWORD}

    resp = requests.post(url, headers=headers, json=payload, timeout=15)

    if resp.status_code >= 400:
        raise FolioAuthError(f"Login failed: {resp.status_code} {resp.text}")

    # The token usually comes back in cookies; requests exposes them via resp.cookies.
    token = resp.cookies.get("folioAccessToken") or resp.cookies.get("okapiToken")

    # Some deployments name the cookie differently, so fall back to scanning them.
    if not token and resp.cookies:
        # Best effort: grab the first cookie whose name looks like a token.
        for k in resp.cookies.keys():
            if "token" in k.lower():
                token = resp.cookies.get(k)
                break

    if not token:
        raise FolioAuthError("Login succeeded but access token not found in cookies.")

    return token
