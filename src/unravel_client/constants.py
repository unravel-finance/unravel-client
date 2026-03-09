import os

WEBSITE = os.getenv("UNRAVEL_BASE_URL", "https://unravel.finance")
BASEAPI = f"{WEBSITE}/api/v1"


def get_headers(api_key: str) -> dict:
    """Build request headers, optionally including Cloudflare Access service token."""
    headers = {"X-API-KEY": api_key}
    cf_client_id = os.getenv("CF_ACCESS_CLIENT_ID")
    cf_client_secret = os.getenv("CF_ACCESS_CLIENT_SECRET")
    if cf_client_id and cf_client_secret:
        headers["CF-Access-Client-Id"] = cf_client_id
        headers["CF-Access-Client-Secret"] = cf_client_secret
    return headers
