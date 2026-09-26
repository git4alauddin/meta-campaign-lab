import io
import json
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from src import inspect_campaign


class CampaignPaginationTests(unittest.TestCase):
    def test_fixture_collects_both_pages_without_network(self):
        output = io.StringIO()
        with (
            patch.dict(os.environ, {"META_ACCESS_TOKEN": "", "META_AD_ACCOUNT_ID": ""}),
            patch.object(inspect_campaign, "urlopen", side_effect=AssertionError("Fixture made a network request")),
            redirect_stdout(output),
        ):
            inspect_campaign.main([])

        printed = output.getvalue()
        self.assertIn("Source: SYNTHETIC fixtures", printed)
        self.assertIn("Campaign pages: 2", printed)
        self.assertIn("Campaigns across all pages: 4", printed)
        campaigns = json.loads(printed[printed.index("[\n"):])
        self.assertEqual(
            [campaign["id"] for campaign in campaigns],
            ["200000000000001", "200000000000002", "200000000000003", "200000000000004"],
        )

    def test_stops_on_a_page_without_next(self):
        campaigns, pages = inspect_campaign.collect_campaigns(
            lambda next_url, page_index: {"data": [{"id": "one"}], "paging": {}}
        )
        self.assertEqual((campaigns, pages), ([{"id": "one"}], 1))

    def test_repeated_next_link_and_invalid_data_are_rejected(self):
        def repeated_link(next_url, page_index):
            return {"data": [], "paging": {"next": "https://example.test/same-page"}}

        with self.assertRaisesRegex(ValueError, "repeated next page"):
            inspect_campaign.collect_campaigns(repeated_link)
        with self.assertRaisesRegex(ValueError, "data list"):
            inspect_campaign.collect_campaigns(lambda next_url, page_index: {"data": {}})
        with self.assertRaisesRegex(ValueError, "invalid paging"):
            inspect_campaign.collect_campaigns(lambda next_url, page_index: {"data": [], "paging": []})

    def test_live_follows_next_link_with_bearer_header_and_without_url_token(self):
        next_link = (
            "https://graph.facebook.com/v26.0/act_123/campaigns?"
            "limit=25&after=cursor_2&access_token=synthetic-url-token"
        )
        responses = [
            io.BytesIO(json.dumps({"data": [{"id": "one"}], "paging": {"next": next_link}}).encode()),
            io.BytesIO(b'{"data": [{"id": "two"}]}'),
        ]
        output = io.StringIO()
        with (
            patch.dict(os.environ, {"META_ACCESS_TOKEN": "synthetic-header-token", "META_AD_ACCOUNT_ID": "act_123"}),
            patch.object(inspect_campaign, "urlopen", side_effect=responses) as mocked_open,
            redirect_stdout(output),
        ):
            inspect_campaign.main(["--source", "live"])

        self.assertEqual(mocked_open.call_count, 2)
        second_request = mocked_open.call_args_list[1].args[0]
        query = parse_qs(urlsplit(second_request.full_url).query)
        self.assertEqual(query["after"], ["cursor_2"])
        self.assertNotIn("access_token", query)
        self.assertEqual(second_request.get_header("Authorization"), "Bearer synthetic-header-token")
        self.assertEqual(mocked_open.call_args_list[1].kwargs["timeout"], 15)
        self.assertIn("Campaign pages: 2", output.getvalue())
        self.assertIn("Campaigns across all pages: 2", output.getvalue())
        self.assertNotIn("synthetic-url-token", output.getvalue())

    def test_live_rejects_paging_to_another_host(self):
        initial = "https://graph.facebook.com/v26.0/act_123/campaigns?limit=25"
        with self.assertRaisesRegex(ValueError, "unexpected campaign paging URL"):
            inspect_campaign.safe_next_url("https://example.test/steal?access_token=x", initial)


if __name__ == "__main__":
    unittest.main()
