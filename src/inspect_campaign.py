import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

API_VERSION = "v26.0"
FIXTURE_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
FIXTURE_PAGES = ("sample_campaigns.json", "sample_campaigns_page_2.json")
MAX_PAGES = 100


def load_fixture_page(next_url, page_index):
    # Fixture links describe pagination; they must never be opened as URLs.
    if page_index >= len(FIXTURE_PAGES):
        raise ValueError("Synthetic campaign response has more pages than fixture files.")
    path = FIXTURE_DIR / FIXTURE_PAGES[page_index]
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    marker = payload.get("_fixture") if isinstance(payload, dict) else None
    if not isinstance(marker, dict) or marker.get("synthetic") is not True:
        raise ValueError("Selected campaign file is not marked as synthetic.")
    return payload


def safe_next_url(next_url, initial_url):
    """Keep pagination on the original Meta endpoint and authenticate by header."""
    initial = urlsplit(initial_url)
    candidate = urlsplit(next_url)
    if (
        candidate.scheme != "https"
        or candidate.hostname != "graph.facebook.com"
        or candidate.path != initial.path
        or candidate.username is not None
        or candidate.password is not None
        or candidate.port is not None
        or candidate.fragment
    ):
        raise ValueError("Meta returned an unexpected campaign paging URL.")
    query = [
        (key, value)
        for key, value in parse_qsl(candidate.query, keep_blank_values=True)
        if key != "access_token"
    ]
    return urlunsplit(("https", "graph.facebook.com", candidate.path, urlencode(query), ""))


def live_page_reader(token, initial_url):
    def read_page(next_url, page_index):
        url = initial_url if next_url is None else safe_next_url(next_url, initial_url)
        request = Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urlopen(request, timeout=15) as response:
                return json.load(response)
        except HTTPError as error:
            raise SystemExit(f"Meta returned HTTP {error.code}. Check the account and read permission.") from None
        except URLError:
            raise SystemExit("Could not reach the Meta API.") from None

    return read_page


def collect_campaigns(read_page):
    campaigns = []
    seen_next_urls = set()
    next_url = None

    for page_index in range(MAX_PAGES):
        payload = read_page(next_url, page_index)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise ValueError("Campaign response must contain a data list.")
        if not all(isinstance(campaign, dict) for campaign in payload["data"]):
            raise ValueError("Campaign data must contain objects.")
        paging = payload.get("paging", {})
        if paging is None:
            paging = {}
        if not isinstance(paging, dict):
            raise ValueError("Campaign response has invalid paging data.")

        campaigns.extend(payload["data"])
        next_url = paging.get("next")
        if next_url is None:
            return campaigns, page_index + 1
        if not isinstance(next_url, str) or not next_url or next_url in seen_next_urls:
            raise ValueError("Campaign response has an invalid or repeated next page.")
        seen_next_urls.add(next_url)

    raise ValueError(f"Campaign response exceeded the {MAX_PAGES}-page safety limit.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect Meta campaigns or synthetic campaign pages.")
    parser.add_argument("--source", choices=("fixture", "live"), default="fixture")
    args = parser.parse_args(argv)

    if args.source == "fixture":
        read_page = load_fixture_page
    else:
        token = os.getenv("META_ACCESS_TOKEN")
        account_id = os.getenv("META_AD_ACCOUNT_ID", "").strip()
        if not token:
            raise SystemExit("Set META_ACCESS_TOKEN in your local .env file.")
        if not (account_id.startswith("act_") and account_id[4:].isdigit()):
            raise SystemExit("Set META_AD_ACCOUNT_ID as act_<account ID> in your local .env file.")
        query = urlencode({"fields": "id,name,objective,status,effective_status", "limit": 25})
        initial_url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/campaigns?{query}"
        read_page = live_page_reader(token, initial_url)

    try:
        campaigns, page_count = collect_campaigns(read_page)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Could not read campaigns: {error}") from None

    source_name = "SYNTHETIC fixtures" if args.source == "fixture" else "LIVE Meta API"
    print(f"Source: {source_name}")
    print(f"Campaign pages: {page_count}")
    print(f"Campaigns across all pages: {len(campaigns)}")
    print(json.dumps(campaigns, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
