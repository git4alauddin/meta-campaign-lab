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

The local `meta-camp` repository is on `main` at commit `487a462` and tracks `origin/main`. Its `origin` remote is the student-provided `https://github.com/git4alauddin/meta-campaign-lab.git`. The agent has not independently fetched live remote contents. Never stage `.env`.

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

- **Status:** Verified by code review and student-reported Python output; **Commit:** Pending.
- **File:** `src/inspect_ads.py`.
- **What and why:** Added a read-only account-level ad request to inspect ads and their parent `adset_id` and `campaign_id` when data exists.
- **Code meaning:** The script reads the token and account ID from the local environment, requests `id,name,adset_id,campaign_id,status,effective_status` from `/ads` with a limit of 25, and prints the first-page count, paging indicator, and returned list. It does not write ad objects or follow additional pages.
- **Verification:** The student ran it in PyCharm and reported `Ads on first page: 0`, `More pages: no`, and `[]`. The agent reviewed the code and its diff against `src/inspect_adsets.py` but did not run a live API request or inspect `.env`. There are no returned parent-child IDs to compare.
- **Recheck:** Run `src/inspect_ads.py` with the local `.env` loaded in PyCharm. If ads later exist, compare their `adset_id` and `campaign_id` values locally to the corresponding lists without sharing account details or tokens.
