# Meta Ads Practical Lab — Experiment 3: Marketing API Fundamentals

**Status:** Ready for hands-on implementation  
**Approach:** Guidance-first; one verified task at a time  
**Stack:** Meta for Developers, Graph API Explorer, Python, `requests`, environment variables  
**Prerequisites:** Experiments 1–2 completed or their essential Ads Manager concepts understood.

## 1. Objective

Learn how to authenticate to the Meta Marketing API and retrieve authorized advertising-account, campaign, ad-set, ad, and performance data. Build a small read-only Python client that can later feed our ingestion pipeline.

**End-to-end demonstration:** Authenticate with an authorized account, enumerate its accessible ad accounts, retrieve campaigns and related objects, request available Insights metrics, and save a sanitized sample response locally.

## 2. Scope and boundaries

**In scope:** Developer app setup; access-token and permission fundamentals; Graph API Explorer; read-only endpoints; Python HTTP requests; response parsing; pagination; API error handling; safe configuration; repeatable manual tests.

**Out of scope:** Publishing or modifying ads; spending money; production app review; long-lived production credential rotation; automated ingestion jobs; database pipelines; Telegram attribution; broker conversions. These belong to later experiments or production hardening.

**Important:** Access to an ad account does not guarantee every permission, endpoint, field, or metric. Some capabilities require app review, business verification, additional permissions, or existing delivery data. Never fabricate live campaign metrics.

## 3. Milestones

### M3.1 — Developer app and API workspace

**Tasks**
1. Confirm access to a Meta developer account and an advertising account you are authorized to inspect.
2. Create or identify an appropriate developer app and configure the Marketing API product or relevant use case as available in the current developer interface.
3. Open Graph API Explorer and identify the API version being used.
4. Record the app ID (not its secret), accessible account identifiers, and the minimum permissions needed for read-only exercises.
5. Document the exact setup steps and any account-specific blockers.

**Acceptance criteria**
- The developer app and Graph API Explorer are accessible.
- At least one authorized account is identified, or a clear blocker and mock-data fallback are documented.
- No secrets appear in the repository, screenshots, logs, or implementation notes.

### M3.2 — Authentication and permissions

**Tasks**
1. Learn the distinction between app ID, app secret, user access token, token expiration, and permission scopes.
2. Generate a token through the authorized developer workflow with the minimum available read permissions (commonly `ads_read`; exact requirements depend on endpoint and account).
3. Make a simple authenticated Graph API request using Graph API Explorer.
4. Inspect token validity and granted permissions using Meta's official debugging tools where available.
5. Create `.env.example` with placeholders and configure `.gitignore` to exclude `.env`.

**Acceptance criteria**
- A read-only authenticated request succeeds, or the exact permission failure is documented.
- The learner can explain why an app ID is not an access token and why tokens must remain secret.
- No credentials are committed.

### M3.3 — Read advertising hierarchy

**Tasks**
1. Retrieve advertising accounts accessible to the token.
2. Select one authorized `act_<AD_ACCOUNT_ID>` account.
3. Retrieve campaigns, then ad sets and ads, requesting a small explicit field list for each.
4. Observe relationships among campaign IDs, ad-set IDs, ad IDs, statuses, and names.
5. Implement the same requests in a minimal Python script using `requests` and an environment-loaded token.
6. Treat empty collections as valid outcomes for an account without campaigns.

**Acceptance criteria**
- Python prints or saves a sanitized hierarchy from the accessible account, or exercises the same parser using clearly labeled fixtures.
- Requested fields and parent-child identifiers are understood.
- The script does not create, edit, publish, or delete advertising objects.

### M3.4 — Insights and response handling

**Tasks**
1. Request available Insights fields, such as spend, impressions, clicks, reach, and date range, from an authorized account or campaign.
2. Compare a campaign-level report with an ad-level report where data exists.
3. Inspect JSON responses, nested structures, omitted fields, and empty results.
4. Normalize selected metrics into a consistent Python representation, preserving report level and date range.
5. Save a sanitized response fixture for repeatable local tests.

**Acceptance criteria**
- The learner can identify the reporting level, time window, and meaning of each retrieved field.
- Empty or unavailable metrics are represented honestly rather than replaced with invented values.
- A sanitized fixture can be parsed without a live API connection.

### M3.5 — Reliability and verification

**Tasks**
1. Follow pagination using response-provided cursors or paging links without logging embedded credentials.
2. Handle invalid/expired tokens, missing permissions, invalid object IDs, network failures, and rate-limit responses.
3. Add request timeouts and conservative retry behavior for transient errors; do not blindly retry permission failures.
4. Verify that error output redacts tokens and sensitive identifiers where appropriate.
5. Run a complete read-only smoke test and document limitations.

**Acceptance criteria**
- Multiple pages can be collected when pagination exists.
- Error scenarios produce useful sanitized diagnostics.
- All successful and blocked tests are documented, with no claim of live-data verification for fixture-only tests.

## 4. Suggested project structure

```text
meta-ads-lab/
  experiment-03/
    README.md
    .env.example
    .gitignore
    requirements.txt
    src/
      config.py
      api_client.py
      inspect_accounts.py
      inspect_insights.py
    tests/
      fixtures/
        sample_accounts.json
        sample_insights.json
      test_response_parsing.py
```

Adapt this layout to the actual repository; do not scaffold all files in advance unless the current task requires them.

## 5. Security and access rules

- Use only accounts and ad assets you own or are explicitly authorized to access.
- Start with least-privilege read permissions; never request write access for a read-only task.
- Store tokens outside source control and avoid exposing them in query logs, screenshots, commit history, or shared fixtures.
- Do not assume developer-mode tokens or test fixtures represent production access.
- Confirm current endpoint fields, permissions, API versions, and rate limits against official Meta documentation during implementation.

## 6. Manual test checklist

- [ ] Developer app and authorized ad-account access confirmed or blockers documented.
- [ ] Authenticated request tested without revealing a token.
- [ ] Ad-account listing retrieved or a labeled fixture used.
- [ ] Campaign → ad set → ad hierarchy inspected.
- [ ] Insights requested for an explicit date range and reporting level.
- [ ] Empty collections and missing fields handled.
- [ ] Pagination tested with a multipage fixture or live response.
- [ ] Expired-token, permission, and network-error paths tested.
- [ ] Repository checked for accidentally committed secrets.
- [ ] README and learning log updated.

## 7. IDE-agent handoff

Follow `TELEGRAM_PROJECT_WORKFLOW.md` as the reference for execution style, adapted to this Meta lab. Work on **one milestone and one small task at a time**. Explain purpose, rough flow, exact file to open, and only the code needed for that step. The student writes and runs code by default. The agent may inspect files and review output; do not install, scaffold, edit, or run services unless explicitly requested.

Use task identifiers such as `m3.f1.developer_app_setup`, `m3.f2.read_only_auth`, and `m3.f3.list_ad_accounts`. Verify each task before proposing a commit. Use explicit `git add` paths, then `git commit -m "m3.fN.task_name"` and `git push` as appropriate. Update the Experiment 3 implementation log after each completed commit. Do not proceed until the current task is verified or its blocker is understood.

## 8. Definition of done

Experiment 3 is complete when the learner has demonstrated a secure read-only Marketing API request, inspected available account hierarchy and Insights data, implemented a minimal Python client, and verified parsing and error-handling paths. Document any API access limitations and retain labeled fixtures for the next experiment.

**Next:** Experiment 4 — Python Campaign Data Pipeline: scheduled extraction, incremental fetching, normalized storage, and reproducible ingestion tests.

## Official references

- Meta Marketing API: https://developers.facebook.com/docs/marketing-apis/
- Meta Graph API: https://developers.facebook.com/docs/graph-api/
- Meta Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Meta Access Tokens: https://developers.facebook.com/docs/facebook-login/guides/access-tokens/
