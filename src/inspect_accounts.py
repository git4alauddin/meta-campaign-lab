import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

API_VERSION = "v26.0"


def main():
    token = os.getenv("META_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Set META_ACCESS_TOKEN in your local run configuration.")

    query = urlencode({
        "fields": "id,name,currency,timezone_name",
        "limit": 25,
    })
    url = f"https://graph.facebook.com/{API_VERSION}/me/adaccounts?{query}"
    request = Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise SystemExit(f"Meta returned HTTP {error.code}. Check the token and ads_read permission.") from None
    except URLError:
        raise SystemExit("Could not reach the Meta API.") from None

    accounts = payload.get("data")
    if not isinstance(accounts, list):
        raise SystemExit("Unexpected response: missing account list.")

    paging = payload.get("paging")
    if isinstance(paging, dict):
        for key in ("next", "previous"):
            link = paging.get(key)
            if isinstance(link, str):
                parts = urlsplit(link)
                safe_query = urlencode(
                    (name, "[REDACTED]" if name.lower() == "access_token" else value)
                    for name, value in parse_qsl(parts.query, keep_blank_values=True)
                )
                paging[key] = urlunsplit(parts._replace(query=safe_query))

    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()