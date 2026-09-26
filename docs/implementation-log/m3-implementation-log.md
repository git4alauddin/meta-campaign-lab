# Experiment 3 — Marketing API implementation log

## Current state

Experiment 3 is in progress. Experiment 1 received an Ads Manager orientation and draft-configuration walkthrough, but its final draft and no-spend checks were not verified. Experiment 2 was deferred by the student's decision to focus on the application and API.

### m3.f1.developer_app_setup

- **Status:** Verified by student report; **Commit:** Pending.
- **What and why:** The student created a Meta developer app and opened Graph API Explorer to establish a workspace for read-only Marketing API exercises.
- **Observed setup:** Graph API version `v26.0`; an authorized ad account was later returned by the account-list request. No app secret or account ID was shared.
- **Recheck:** Open Graph API Explorer, select the app, and confirm the version. App dashboard details were not independently inspected by the agent.

### m3.f2.read_only_auth

- **Status:** Verified by student report; **Commit:** Pending.
- **What and why:** The student generated a user access token with `ads_read` and sent `GET /me/adaccounts?fields=id,name,currency,timezone_name` in Graph API Explorer to check read access.
- **Evidence:** The student reported a successful response containing data and paging. The token and raw response were not shared.
- **Concept:** `ads_read` permits this initial read exercise; token possession and permissions do not imply write access or available delivery metrics.
- **Recheck:** Repeat the same GET request in Explorer and inspect the result locally, without recording tokens or account identifiers.

### m3.f3.list_ad_accounts

- **Status:** Read-only request verified by code review and student-run summary; expanded JSON display reviewed in code, with exact response comparison pending; **Commit:** Pending.
- **Files:** `src/inspect_accounts.py`, `.env.example`, `.gitignore`; the local `.env` is ignored by Git.
- **What and why:** A standard-library Python script repeats the read-only account-list request using a bearer token from `META_ACCESS_TOKEN`. It requests one page with a 15-second timeout, parses the JSON, redacts any `access_token` query parameter in paging links, and prints the returned account data and paging structure for comparison with Graph API Explorer.
- **Evidence:** The student first ran the summary version in PyCharm and reported `Accounts on first page: 1` and `More pages: no`. The expanded JSON display was then reviewed in code; the student described it as working but did not share a field-by-field comparison. PyCharm's configured interpreter was checked as Python 3.13.7 in this project's `.venv`. The agent did not run a live request or inspect `.env`.
- **Code meaning:** The URL selects fields and page size; the bearer header authenticates the read; `json.load` parses the response; `data` contains the account records and `paging` holds pagination metadata. The script changes only its local copy of paging links before display.
- **Limitations:** The script does not yet fetch additional pages, campaign/ad-set/ad hierarchy, or Insights. It gives a generic HTTP error and does not distinguish all Meta API failure types. Those are later tasks.
- **Recheck:** Run `src/inspect_accounts.py` with `META_ACCESS_TOKEN` loaded from the local `.env` by PyCharm and compare the locally displayed `data` and `paging` with the same `v26.0` Explorer request and `limit=25`.

## Repository state

The local `meta-camp` folder has an initialized Git repository on `main` and an `origin` remote set to the student-provided `https://github.com/git4alauddin/meta-campaign-lab.git`. No local commit existed at the time of this entry. Remote contents could not be verified from the agent environment because GitHub was unreachable. Review explicit staged paths before the first commit; never stage `.env`.
