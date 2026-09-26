# Experiment 3 — Marketing API implementation log

## Current state

Experiment 3 is in progress. Experiment 1 received an Ads Manager orientation and draft-configuration walkthrough, but its final draft and no-spend checks were not verified. Experiment 2 was deferred by the student's decision to focus on the application and API.

### m3.f1.developer_app_setup

- **Status:** Verified by student report; **Commit:** `d4c5adc` (recorded with the next feature, per the agreed log convention).
- **What and why:** The student created a Meta developer app and opened Graph API Explorer to establish a workspace for read-only Marketing API exercises.
- **Observed setup:** Graph API version `v26.0`; an authorized ad account was later returned by the account-list request. No app secret or account ID was shared.
- **Recheck:** Open Graph API Explorer, select the app, and confirm the version. App dashboard details were not independently inspected by the agent.

### m3.f2.read_only_auth

- **Status:** Verified by student report; **Commit:** `d4c5adc` (recorded with the next feature, per the agreed log convention).
- **What and why:** The student generated a user access token with `ads_read` and sent `GET /me/adaccounts?fields=id,name,currency,timezone_name` in Graph API Explorer to check read access.
- **Evidence:** The student reported a successful response containing data and paging. The token and raw response were not shared.
- **Concept:** `ads_read` permits this initial read exercise; token possession and permissions do not imply write access or available delivery metrics.
- **Recheck:** Repeat the same GET request in Explorer and inspect the result locally, without recording tokens or account identifiers.

### m3.f3.list_ad_accounts

- **Status:** Read-only request verified by code review and student-run summary; expanded JSON display reviewed in code, with exact response comparison pending; **Commit:** `d4c5adc` (recorded with the next feature, per the agreed log convention).
- **Files:** `src/inspect_accounts.py`, `.env.example`, `.gitignore`; the local `.env` is ignored by Git.
- **What and why:** A standard-library Python script repeats the read-only account-list request using a bearer token from `META_ACCESS_TOKEN`. It requests one page with a 15-second timeout, parses the JSON, redacts any `access_token` query parameter in paging links, and prints the returned account data and paging structure for comparison with Graph API Explorer.
- **Evidence:** The student first ran the summary version in PyCharm and reported `Accounts on first page: 1` and `More pages: no`. The expanded JSON display was then reviewed in code; the student described it as working but did not share a field-by-field comparison. PyCharm's configured interpreter was checked as Python 3.13.7 in this project's `.venv`. The agent did not run a live request or inspect `.env`.
- **Code meaning:** The URL selects fields and page size; the bearer header authenticates the read; `json.load` parses the response; `data` contains the account records and `paging` holds pagination metadata. The script changes only its local copy of paging links before display.
- **Limitations:** The script does not yet fetch additional pages, campaign/ad-set/ad hierarchy, or Insights. It gives a generic HTTP error and does not distinguish all Meta API failure types. Those are later tasks.
- **Recheck:** Run `src/inspect_accounts.py` with `META_ACCESS_TOKEN` loaded from the local `.env` by PyCharm and compare the locally displayed `data` and `paging` with the same `v26.0` Explorer request and `limit=25`.

## Repository state

The local `meta-camp` repository is on `main` at commit `8e1f081` and tracks `origin/main`. Its `origin` remote is the student-provided `https://github.com/git4alauddin/meta-campaign-lab.git`. The agent has not independently fetched live remote contents. Never stage `.env`.

### m3.f4.list_campaigns

- **Status:** Verified by code review and student-reported Explorer and Python output; **Commit:** `09fdf54` (recorded with the next feature, per the agreed log convention).
- **What and why:** The student sent a read-only campaign-list request for the authorized ad account to discover the response shape before coding it.
- **Evidence:** The student shared a sanitized response of `{"data": []}`. This confirms an empty campaign list for that request. It does not establish why no campaigns were returned or whether an unpublished Ads Manager draft exists.
- **Python implementation:** The student added `src/inspect_campaign.py`, using `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID` from local configuration. An initial run stopped at local account-ID validation; the student corrected the value. The agent reviewed the read-only code but did not run the live request or inspect `.env`.
- **Verification:** The student reported `Campaigns on first page: 0`, `More pages: no`, and `[]`, matching the earlier Explorer response. An empty list is handled as a successful result. The code requests only one page and makes no write request.
- **Recheck:** Run `src/inspect_campaign.py` with the local `.env` loaded in PyCharm and compare the count and paging indicator with the same account-level Explorer GET. If campaigns later exist, inspect returned fields locally without sharing IDs or names.

### m3.f5.list_ad_sets

- **Status:** Verified by code review and student-reported Python output; **Commit:** `487a462` (recorded with the next feature, per the agreed log convention).
- **File:** `src/inspect_adsets.py`.
- **What and why:** Added a read-only account-level ad-set request to extend the advertising hierarchy and expose each ad set's parent `campaign_id` when data exists.
- **Code meaning:** The script reads `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID` from the local environment, requests `id,name,campaign_id,status,effective_status` from `/adsets` with a limit of 25, and prints the first-page count, whether another page exists, and the returned list. It does not modify ads or retrieve additional pages.
- **Verification:** The student ran it in PyCharm and reported `Ad sets on first page: 0`, `More pages: no`, and `[]`. The agent reviewed the file and its diff against `src/inspect_campaign.py` but did not run a live API request or inspect `.env`. This is a valid empty result for that request; no parent-child IDs could be compared yet.
- **Recheck:** Run `src/inspect_adsets.py` with the local `.env` loaded in PyCharm. If ad sets later exist, compare their `campaign_id` values to the campaign list locally without sharing account details or tokens.

### m3.f6.list_ads

- **Status:** Verified by code review and student-reported Python output; **Commit:** `64f8c0b` (recorded with the next feature, per the agreed log convention).
- **File:** `src/inspect_ads.py`.
- **What and why:** Added a read-only account-level ad request to inspect ads and their parent `adset_id` and `campaign_id` when data exists.
- **Code meaning:** The script reads the token and account ID from the local environment, requests `id,name,adset_id,campaign_id,status,effective_status` from `/ads` with a limit of 25, and prints the first-page count, paging indicator, and returned list. It does not write ad objects or follow additional pages.
- **Verification:** The student ran it in PyCharm and reported `Ads on first page: 0`, `More pages: no`, and `[]`. The agent reviewed the code and its diff against `src/inspect_adsets.py` but did not run a live API request or inspect `.env`. There are no returned parent-child IDs to compare.
- **Recheck:** Run `src/inspect_ads.py` with the local `.env` loaded in PyCharm. If ads later exist, compare their `adset_id` and `campaign_id` values locally to the corresponding lists without sharing account details or tokens.

### m3.f7.read_account_insights

- **Status:** Verified by code review and student-reported Explorer and Python output; **Commit:** `aefb4ec` (recorded with the next feature, per the agreed log convention).
- **File:** `src/inspect_insights.py`.
- **What and why:** Added a read-only account-level Insights request for September 1-26, 2026 to establish a fixed reporting window for later analytics work.
- **Code meaning:** The script reads the token and account ID from the local environment, requests `date_start,date_stop,spend,impressions,clicks,reach` with `level=account`, the fixed `time_range`, and a limit of 25. It prints the selected range, first-page row count, paging indicator, and returned rows. It does not write ad objects or follow additional pages.
- **Verification:** The student reported `{"data": []}` for the same request in Graph API Explorer, then ran the Python script and reported `Insights range: 2026-09-01 to 2026-09-26`, `Insights rows on first page: 0`, `More pages: no`, and `[]`. The agent reviewed the code but did not run a live API request or inspect `.env`.
- **Limitations:** The empty response contains no metric values; it must not be interpreted as a row of zero-valued metrics. Normalization of nonempty results and comparison across reporting levels remain unverified.
- **Recheck:** Run `src/inspect_insights.py` with the local `.env` loaded in PyCharm, and compare the date range and row count with the same Explorer GET. Do not share tokens or account details.

### m3.f8.synthetic_response_fixtures

- **Status:** Fixture files created and locally validated; **Commit:** `8e1f081` (recorded with the next feature, per the agreed log convention).
- **Files:** `tests/fixtures/README.md` and 16 JSON fixtures covering an account, two campaign pages, ad sets, ads, aggregate account/campaign/ad-set/ad Insights, seven daily account rows, 21 daily campaign rows, explicit-zero and empty cases, and illustrative expired-token, permission, and rate-limit error bodies.
- **What and why:** The live account returned no campaign, ad-set, ad, or Insights rows. These deliberately invented responses provide nonempty hierarchy and metrics for offline parser, pagination, and error-handling exercises without implying live ad delivery or spend.
- **Data meaning:** Four synthetic campaigns, five ad sets, and five ads support traffic-campaign comparison, a different awareness objective, and a no-delivery hierarchy. Three campaigns have invented delivery between September 20-26, 2026 within the September 1-26 aggregate window. Account, campaign, ad-set, ad, and daily spend, impressions, and clicks reconcile to 100.00, 14000, and 400. Reach is deliberately non-additive; one campaign/day row omits reach to distinguish missing from zero. The top-level `_fixture` marker is local metadata, not a Meta API field. Paging URLs and error details are illustrative and contain no token.
- **Verification:** All 16 JSON files parsed with PowerShell `ConvertFrom-Json` and contained `_fixture.synthetic = true`. Local checks confirmed hierarchy parent links, row counts, aggregate and per-day additive totals, the missing-reach case, and the preserved empty fixture. The agent did not run the Python client against these files or make a live API request.
- **Limitations:** Synthetic error codes and HTTP status metadata are test inputs, not a guarantee of Meta's exact responses. A network failure has no JSON body and will need a simulated transport exception. Fixtures alone do not verify pagination or normalization code.
- **Recheck:** Inspect `tests/fixtures/README.md`, parse each JSON file locally, and verify IDs and metric totals before using the samples in parser tests. Never send fixture URLs to Meta.

### m3.f9.insights_source_and_parser

- **Status:** Locally verified with fixtures and a mocked live request; student reports the PyCharm fixture and live account-level runs worked; **Commit:** `2e7223c` (recorded with the next feature, per the agreed log convention).
- **Files:** `src/inspect_insights.py`, `tests/test_insights_parsing.py`.
- **What and why:** The Insights script now defaults to an offline synthetic fixture and uses `--source live` for an explicit Meta GET. `--level account|campaign|adset|ad` selects the reporting level and matching aggregate fixture. Both sources feed the same normalization path.
- **Code meaning:** Normalization keeps the report level, date range, and parent IDs; parses spend with `Decimal` and count metrics as integers; and leaves omitted metrics as `None`. It rejects malformed dates, IDs, and metric values. Fixture mode checks the synthetic marker before use and needs no token or network. Output names its source so sample values cannot be mistaken for live performance.
- **Verification:** Six standard-library unit tests passed using PyCharm's configured Python 3.13.7 environment. They covered account and hierarchy levels, empty versus explicit zero and missing reach, malformed input, fixture mode without credentials/network, and a mocked live request with the same account-level query and timeout. A direct offline script run from `src/` printed one synthetic account row with spend `100.00`, impressions `14000`, clicks `400`, reach `9000`, and no next page. The student reports both the PyCharm fixture run and a later `--source live --level account` run worked after regenerating the token. The student did not share live row counts or a raw response. No live Meta request was made by the agent; `.env` was not inspected.
- **Limitations:** Only the first Insights page is processed. Daily fixture selection, KPI calculations, API error classification, and nonempty live Insights parsing remain for later tasks.
- **Recheck:** Run `src/inspect_insights.py` in PyCharm with no script parameters and confirm `Source: SYNTHETIC fixture` and one account row. Optionally use `--level ad` for four synthetic ad rows. Use `--source live` only when intentionally checking the authorized Meta account.

### m3.f10.campaign_pagination

- **Status:** Implemented and locally verified; student PyCharm run pending; **Commit:** Pending.
- **Files:** `src/inspect_campaign.py`, `tests/test_campaign_pagination.py`.
- **What and why:** The campaign inspector now defaults to local synthetic fixtures and collects both campaign pages by following the presence of `paging.next`, producing one four-campaign list. `--source live` follows Meta campaign pages with the same collection logic; the original read-only campaign query remains explicit.
- **Code meaning:** Fixture paging selects local files and never opens the synthetic link. Live paging accepts only HTTPS links to the same Graph campaign endpoint, removes any URL access token in favor of the bearer header, and never prints paging URLs. Repeated links and malformed pages fail clearly; a 100-page limit prevents an unbounded loop.
- **Verification:** Five pagination tests passed, along with the six existing Insights tests, using PyCharm's configured Python 3.13.7 environment. They covered the four campaigns across two local pages without a token or network, stopping after a page without `next`, rejecting malformed or repeated pages, a mocked two-page live request with bearer authentication and no URL token, and a rejected cross-host link. The agent did not call the live Meta API or inspect `.env`.
- **Limitations:** The live account previously returned no campaigns, so live multi-page behavior is verified only with mocks. The fixture mode is intentionally tied to the two known local files; generic fixture routing and broader API error classification remain for later tasks.
- **Recheck:** Run `src/inspect_campaign.py` in PyCharm with no script parameters. Confirm `Source: SYNTHETIC fixtures`, `Campaign pages: 2`, and `Campaigns across all pages: 4`. Use `--source live` only for an intentional authorized read.
