import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_VERSION = "v26.0"
SINCE_DATE = "2026-09-01"
UNTIL_DATE = "2026-09-26"


def main():
    token = os.getenv("META_ACCESS_TOKEN")
    account_id = os.getenv("META_AD_ACCOUNT_ID", "").strip()

    if not token:
        raise SystemExit("Set META_ACCESS_TOKEN in your local .env file.")
    if not (account_id.startswith("act_") and account_id[4:].isdigit()):
        raise SystemExit("Set META_AD_ACCOUNT_ID as act_<account ID> in your local .env file.")

    query = urlencode({
        "fields": "date_start,date_stop,spend,impressions,clicks,reach",
        "level": "account",
        "time_range": json.dumps({"since": SINCE_DATE, "until": UNTIL_DATE}),
        "limit": 25,
    })
    url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/insights?{query}"
    request = Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except HTTPError as error:
        raise SystemExit(f"Meta returned HTTP {error.code}. Check the account and read permission.") from None
    except URLError:
        raise SystemExit("Could not reach the Meta API.") from None

    rows = payload.get("data")
    if not isinstance(rows, list):
        raise SystemExit("Unexpected response: missing Insights list.")

    print(f"Insights range: {SINCE_DATE} to {UNTIL_DATE}")
    print(f"Insights rows on first page: {len(rows)}")
    print(f"More pages: {'yes' if (payload.get('paging') or {}).get('next') else 'no'}")
    print(json.dumps(rows, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
