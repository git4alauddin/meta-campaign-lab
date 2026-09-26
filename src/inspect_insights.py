import argparse
import json
import os
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_VERSION = "v26.0"
SINCE_DATE = "2026-09-01"
UNTIL_DATE = "2026-09-26"
FIXTURE_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
FIXTURES = {
    "account": "sample_insights.json",
    "campaign": "sample_insights_campaign.json",
    "adset": "sample_insights_adset.json",
    "ad": "sample_insights_ad.json",
}
LEVEL_ID_FIELDS = {
    "account": (),
    "campaign": ("campaign_id",),
    "adset": ("adset_id", "campaign_id"),
    "ad": ("ad_id", "adset_id", "campaign_id"),
}


def load_fixture(level):
    path = FIXTURE_DIR / FIXTURES[level]
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)

    marker = payload.get("_fixture") if isinstance(payload, dict) else None
    if not isinstance(marker, dict) or marker.get("synthetic") is not True:
        raise ValueError("Selected file is not marked as synthetic.")
    if marker.get("level") != level:
        raise ValueError("Fixture reporting level does not match the request.")
    return payload


def fetch_live(level):
    token = os.getenv("META_ACCESS_TOKEN")
    account_id = os.getenv("META_AD_ACCOUNT_ID", "").strip()

    if not token:
        raise SystemExit("Set META_ACCESS_TOKEN in your local .env file.")
    if not (account_id.startswith("act_") and account_id[4:].isdigit()):
        raise SystemExit("Set META_AD_ACCOUNT_ID as act_<account ID> in your local .env file.")

    fields = ["date_start", "date_stop", "spend", "impressions", "clicks", "reach"]
    fields.extend(LEVEL_ID_FIELDS[level])
    query = urlencode({
        "fields": ",".join(fields),
        "level": level,
        "time_range": json.dumps({"since": SINCE_DATE, "until": UNTIL_DATE}),
        "limit": 25,
    })
    url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/insights?{query}"
    request = Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except HTTPError as error:
        raise SystemExit(f"Meta returned HTTP {error.code}. Check the account and read permission.") from None
    except URLError:
        raise SystemExit("Could not reach the Meta API.") from None


def _metric_decimal(value, name):
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a decimal value.")
    try:
        result = Decimal(str(value))
    except InvalidOperation:
        raise ValueError(f"{name} must be a decimal value.") from None
    if not result.is_finite():
        raise ValueError(f"{name} must be finite.")
    return result


def _metric_count(value, name):
    if value is None:
        return None
    if isinstance(value, bool) or not (
        isinstance(value, int) and value >= 0
        or isinstance(value, str) and value.isascii() and value.isdecimal()
    ):
        raise ValueError(f"{name} must be a nonnegative integer.")
    return int(value)


def normalize_insights(payload, level):
    if level not in LEVEL_ID_FIELDS:
        raise ValueError("Unknown reporting level.")
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("Insights response must contain a data list.")

    normalized = []
    for index, row in enumerate(payload["data"]):
        if not isinstance(row, dict):
            raise ValueError(f"Insight row {index} must be an object.")

        start, stop = row.get("date_start"), row.get("date_stop")
        try:
            if not isinstance(start, str) or not isinstance(stop, str):
                raise ValueError
            if date.fromisoformat(start) > date.fromisoformat(stop):
                raise ValueError
        except ValueError:
            raise ValueError(f"Insight row {index} has an invalid date range.") from None

        record = {
            "level": level,
            "date_start": start,
            "date_stop": stop,
        }
        for field in ("campaign_id", "adset_id", "ad_id"):
            value = row.get(field)
            if value is not None:
                if not isinstance(value, str) or not value:
                    raise ValueError(f"Insight row {index} has an invalid {field}.")
                record[field] = value
        for field in LEVEL_ID_FIELDS[level]:
            if field not in record:
                raise ValueError(f"Insight row {index} is missing {field}.")

        record["spend"] = _metric_decimal(row.get("spend"), "spend")
        for field in ("impressions", "clicks", "reach"):
            record[field] = _metric_count(row.get(field), field)
        normalized.append(record)
    return normalized


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect read-only Meta Insights or synthetic fixtures.")
    parser.add_argument("--source", choices=("fixture", "live"), default="fixture")
    parser.add_argument("--level", choices=tuple(FIXTURES), default="account")
    args = parser.parse_args(argv)

    try:
        payload = load_fixture(args.level) if args.source == "fixture" else fetch_live(args.level)
        rows = normalize_insights(payload, args.level)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Could not read Insights data: {error}") from None

    paging = payload.get("paging") or {}
    if not isinstance(paging, dict):
        raise SystemExit("Unexpected response: invalid paging value.")

    source_name = f"SYNTHETIC fixture ({FIXTURES[args.level]})" if args.source == "fixture" else "LIVE Meta API"
    print(f"Source: {source_name}")
    print(f"Insights level: {args.level}")
    print(f"Insights range: {SINCE_DATE} to {UNTIL_DATE}")
    print(f"Insights rows on first page: {len(rows)}")
    print(f"More pages: {'yes' if paging.get('next') else 'no'}")
    print(json.dumps(rows, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
