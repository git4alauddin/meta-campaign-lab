import io
import json
import os
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from src import inspect_insights


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def read_fixture(name):
    with (FIXTURE_DIR / name).open(encoding="utf-8") as file:
        return json.load(file)


class InsightsParsingTests(unittest.TestCase):
    def test_account_values_keep_types_and_reporting_window(self):
        rows = inspect_insights.normalize_insights(read_fixture("sample_insights.json"), "account")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["level"], "account")
        self.assertEqual((rows[0]["date_start"], rows[0]["date_stop"]), ("2026-09-01", "2026-09-26"))
        self.assertEqual(rows[0]["spend"], Decimal("100.00"))
        self.assertEqual((rows[0]["impressions"], rows[0]["clicks"], rows[0]["reach"]), (14000, 400, 9000))

    def test_other_levels_preserve_parent_ids(self):
        for level, filename, id_field, count in (
            ("campaign", "sample_insights_campaign.json", "campaign_id", 3),
            ("adset", "sample_insights_adset.json", "adset_id", 4),
            ("ad", "sample_insights_ad.json", "ad_id", 4),
        ):
            with self.subTest(level=level):
                rows = inspect_insights.normalize_insights(read_fixture(filename), level)
                self.assertEqual(len(rows), count)
                self.assertTrue(all(row[id_field] for row in rows))
                self.assertTrue(all(row["level"] == level for row in rows))
        self.assertEqual(rows[0]["campaign_id"], "200000000000001")
        self.assertEqual(rows[0]["adset_id"], "300000000000001")

    def test_empty_zero_and_missing_reach_stay_distinct(self):
        empty = inspect_insights.normalize_insights(read_fixture("sample_insights_empty.json"), "account")
        zero = inspect_insights.normalize_insights(read_fixture("sample_insights_zero.json"), "campaign")
        daily = read_fixture("sample_insights_campaign_daily.json")["data"]
        missing = next(row for row in daily if "reach" not in row)
        normalized_missing = inspect_insights.normalize_insights({"data": [missing]}, "campaign")

        self.assertEqual(empty, [])
        self.assertEqual((zero[0]["spend"], zero[0]["impressions"], zero[0]["reach"]), (Decimal("0.00"), 0, 0))
        self.assertIsNone(normalized_missing[0]["reach"])

    def test_invalid_rows_are_rejected(self):
        cases = (
            ({"data": {}}, "account"),
            ({"data": [{"date_start": "2026-09-26", "date_stop": "2026-09-01"}]}, "account"),
            ({"data": [{"date_start": "2026-09-01", "date_stop": "2026-09-26"}]}, "campaign"),
            ({"data": [{"date_start": "2026-09-01", "date_stop": "2026-09-26", "spend": "NaN"}]}, "account"),
            ({"data": [{"date_start": "2026-09-01", "date_stop": "2026-09-26", "clicks": "2.5"}]}, "account"),
        )
        for payload, level in cases:
            with self.subTest(payload=payload, level=level):
                with self.assertRaises(ValueError):
                    inspect_insights.normalize_insights(payload, level)

    def test_fixture_mode_needs_no_token_or_network(self):
        default_output = io.StringIO()
        ad_output = io.StringIO()
        with (
            patch.dict(os.environ, {"META_ACCESS_TOKEN": "", "META_AD_ACCOUNT_ID": ""}),
            patch.object(inspect_insights, "urlopen", side_effect=AssertionError("Network request in fixture mode")),
        ):
            with redirect_stdout(default_output):
                inspect_insights.main([])
            with redirect_stdout(ad_output):
                inspect_insights.main(["--source", "fixture", "--level", "ad"])

        self.assertIn("Source: SYNTHETIC fixture (sample_insights.json)", default_output.getvalue())
        self.assertIn("Insights rows on first page: 1", default_output.getvalue())
        self.assertIn("Source: SYNTHETIC fixture (sample_insights_ad.json)", ad_output.getvalue())
        self.assertIn("Insights rows on first page: 4", ad_output.getvalue())

    def test_live_mode_is_explicit_and_keeps_the_read_only_query(self):
        output = io.StringIO()
        with (
            patch.dict(os.environ, {"META_ACCESS_TOKEN": "synthetic-test-token", "META_AD_ACCOUNT_ID": "act_123"}),
            patch.object(inspect_insights, "urlopen", return_value=io.BytesIO(b'{"data": []}')) as mocked_open,
            redirect_stdout(output),
        ):
            inspect_insights.main(["--source", "live"])

        request = mocked_open.call_args.args[0]
        query = parse_qs(urlparse(request.full_url).query)
        self.assertEqual(query["level"], ["account"])
        self.assertEqual(query["fields"], ["date_start,date_stop,spend,impressions,clicks,reach"])
        self.assertEqual(request.get_header("Authorization"), "Bearer synthetic-test-token")
        self.assertEqual(mocked_open.call_args.kwargs["timeout"], 15)
        self.assertIn("Source: LIVE Meta API", output.getvalue())
        self.assertIn("Insights rows on first page: 0", output.getvalue())


if __name__ == "__main__":
    unittest.main()
