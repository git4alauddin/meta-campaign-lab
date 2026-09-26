# Meta Ads Practical Lab — Experiment 6: Meta → Telegram Integration

**Status:** Ready for hands-on implementation  
**Prerequisites:** Meta Experiments 1–5; Telegram Experiments 1–5 (Experiment 6 mock affiliate events optional)  
**Stack:** Python, FastAPI (only where needed), SQLite, pytest, existing Meta ingestion and Telegram bot/event modules  
**Mode:** Guidance-first. Implement, verify, commit and log one small task at a time.

## Objective

Connect the Meta campaign data pipeline to the existing Telegram referral, membership and engagement system. Produce a defensible cross-platform funnel that joins campaign-level advertising spend with observed Telegram outcomes, while clearly distinguishing **verified Telegram events**, **Meta-reported aggregate metrics**, **self-recorded referral attribution**, and **simulated affiliate conversions**.

**Final demonstration:** Select a sample Meta campaign/ad, create a campaign-tagged Telegram entry link, follow it as a real test user, verify the bot start and channel join, then inspect a unified dashboard showing campaign spend and the Telegram funnel. The lab must work end-to-end with mock Meta data and no paid advertising.

## Scope and boundaries

**In scope:** stable campaign/ad ID mapping, safe referral-link generation, Telegram deep-link intake, existing first-valid-touch attribution, cross-platform data contracts, campaign-to-Telegram joins, aggregate funnel reporting, optional mock affiliate outcomes, reconciliation, privacy, failure handling and documented replacement of mock adapters.

**Out of scope:** assuming Meta exposes individual ad-click identities; claiming a Telegram bot start proves a Meta ad click; reconstructing user-level journeys from aggregate Meta Insights; launching paid campaigns; production financial promotions; changing the Telegram membership/admission system; replacing existing Meta ingestion or analytics components; and real broker conversions without authorized broker postbacks.

**Important distinction:** Meta's campaign/ad reporting and Telegram's bot/membership events come from separate systems. A tagged deep link provides our own attribution evidence, not independently verified person-level Meta click attribution. An ordinary Meta ad click cannot be assumed to preserve a per-person ID into Telegram. Draft/mock campaigns cannot establish real ad delivery or campaign performance.

## M6.1 — Integration contracts and campaign identity

**Goal:** Connect existing data models without creating a second campaign registry or event store.

Tasks:
- Inspect the Meta Experiment 4 tables, Experiment 5 query layer and Telegram Experiment 3 attribution schema before making changes.
- Define a canonical mapping between Meta account, campaign, ad set and ad IDs and the existing Telegram referral-token records. Preserve IDs as strings, including any platform prefixes where relevant.
- Distinguish `source_type` (`mock_meta`, `meta_api`) and `event_provenance` (`telegram_verified`, `self_attributed`, `meta_aggregate`, `mock_affiliate`).
- Define reporting grain and time handling: account reporting timezone, Telegram event timestamps in UTC, daily rollups, currency and reporting windows.
- Add a migration or adapter for existing mock campaign references rather than silently rewriting historical referral records.
- Prepare fixtures with two campaigns, multiple ads, distinct referral tokens and known Telegram outcomes.

Acceptance criteria:
- Every valid referral token resolves to one known campaign/ad hierarchy and source type.
- Unmapped, inactive or deleted campaign records have explicit states; no fabricated mapping is created.
- Existing Meta and Telegram tests continue to pass after schema changes.

## M6.2 — Campaign-tagged entry links and real Telegram intake

**Goal:** Build a reproducible, observable entry path from a campaign reference to the real Telegram bot.

Tasks:
- Create a small local CLI/admin-only endpoint to issue a Telegram deep link for an allowlisted campaign/ad using the existing opaque, URL-safe token mechanism.
- Reuse Telegram Experiment 3's `/start <TOKEN>` parsing and first-valid-touch attribution; do not add competing attribution logic.
- Record link issuance and subsequent bot starts separately; do not invent click events merely because a link was generated.
- Reuse the Telegram Experiment 2 join-request and verified membership handlers; distinguish bot start, join request, approval and actual join.
- Provide a controlled test path for a real Telegram user following a mock-campaign link, starting the bot and joining the private test channel.
- Document link forwarding, repeated `/start`, returning users, invalid tokens and users entering Telegram through another route.

Acceptance criteria:
- A test user can follow a tagged link and appear under the expected mock campaign in the existing Telegram event store.
- Verified membership is counted only after Telegram confirms the join.
- Repeating the same deep link does not create duplicate users or duplicate acquisitions.
- Untagged users remain unattributed; forwarded links are treated as self-recorded attribution, not verified Meta click proof.

## M6.3 — Unified read-only data service

**Goal:** Join Meta aggregates and Telegram events without mixing incompatible metrics.

Tasks:
- Build a read-only service/view combining campaign/ad hierarchy, Meta daily insights and Telegram referral/engagement aggregates.
- Aggregate Telegram events by mapped campaign/ad and event date; provide an explicit policy for cohort-date versus event-date reporting.
- Keep Meta-reported link clicks and Telegram bot starts as separate metrics. Compute observed ratios only when the denominator is available and compatible.
- Calculate spend per attributed bot start and spend per verified attributed join as **observational blended ratios**, with coverage and attribution caveats. Do not call them Meta-verified conversion costs.
- Support absent spend, multiple currencies, partial data, mismatched timezones and revised historical Meta Insights.
- Optionally join Telegram Experiment 6 mock affiliate registrations, mock CPA approvals and mock commissions, visibly labeled as simulated.

Acceptance criteria:
- Known fixtures produce independently verifiable campaign-level spend, bot starts, join requests, verified joins and engagement totals.
- A campaign with no tagged users remains visible with zero observed tagged outcomes, not missing campaign data.
- Unattributed Telegram users are shown separately; unknown Meta values remain missing rather than converted to zero.
- No double counting when multiple reporting grains or late-arriving events are present.

## M6.4 — End-to-end dashboard and reporting

**Goal:** Make the cross-platform funnel inspectable from one place.

Tasks:
- Extend the existing Experiment 5 dashboard rather than building a second standalone reporting UI.
- Add filters for campaign, ad set, ad, source type, reporting dates and attribution/cohort view.
- Display Meta spend, impressions and reported clicks alongside tagged bot starts, join requests, verified joins, membership exits and tracked offer interactions.
- Add a funnel visualization and drill-down to the underlying aggregate/event records where permitted; label each metric's source and confidence.
- Show last successful Meta sync, last Telegram event ingestion and any partial-data or unmapped-ID warnings.
- Export a CSV/Markdown report with reporting period, source types, attribution policy, currency, refresh times and caveats.

Acceptance criteria:
- Dashboard totals reconcile with database queries and exported reports.
- Filters do not accidentally add rates or combine different currencies.
- Mock-data demonstrations work offline and are unmistakably labeled as simulated.
- No access tokens, private user details or unredacted invite tokens appear in reports/screenshots.

## M6.5 — Reliability, privacy and integration verification

**Goal:** Demonstrate correctness under common cross-platform failure modes.

Tasks:
- Test invalid/expired referral tokens, link forwarding, repeated bot starts, duplicated Telegram updates, delayed membership events and returning users.
- Test Meta API unavailability, expired credentials, rate limiting, missing historical insights, deleted/renamed campaigns and late metric revisions using fixtures.
- Test idempotent imports and replay: rerunning the same Meta ingestion or Telegram update must not inflate counts.
- Validate least-privilege Meta permissions, encrypted/secret-managed credentials, no secrets in Git and minimal retention of Telegram personal data.
- Provide a documented test-user data deletion procedure and distinguish aggregate reporting from personal data.
- Add a manual reconciliation script that reports unmapped campaign IDs, untagged Telegram users and mismatched date windows.
- Perform a final walkthrough from mock campaign → generated link → real Telegram bot start → verified channel join → unified dashboard. Optionally replay mock affiliate outcomes.
- Before any real Forex/financial advertisement, separately verify the intended market's laws, broker authorization and current Meta financial advertising requirements; this experiment does not authorize a live campaign.

Acceptance criteria:
- The complete mock-to-real-Telegram walkthrough succeeds without paid ads.
- Unit and integration tests pass; retries and replays do not duplicate attribution or spend.
- Reports disclose data provenance and limitations, and all failures have visible diagnostics.
- The mock Meta adapter can later be replaced with authorized real Meta data without changing Telegram intake or attribution policy.

## Suggested project layout (adapt to existing repositories)

```text
meta-ads-lab/
  experiment-06/
    src/
      campaign_mapping.py
      referral_link_service.py
      unified_queries.py
      funnel_metrics.py
      reconciliation.py
      integration_cli.py
    tests/
      fixtures/
      test_campaign_mapping.py
      test_referral_integration.py
      test_unified_queries.py
      test_reconciliation.py
      test_end_to_end.py
    README.md
```

Reuse existing Meta ingestion, dashboard, Telegram bot, referral, membership and event modules. The layout above contains only new integration code; do not copy those modules into this directory.

## Data contract (adapt, do not duplicate)

| Concept | Minimum fields | Source |
|---|---|---|
| Campaign identity | source_type, account_id, campaign_id, ad_set_id, ad_id | Existing Meta/mock registry |
| Referral mapping | opaque_token_id, source_type, campaign_id, ad_set_id, ad_id, issued_at, status | Existing Telegram attribution + adapter |
| Telegram funnel event | event_id, telegram_user_id, event_type, event_at_utc, referral_token_id, provenance | Existing Telegram event store |
| Meta daily insight | account_id, campaign_id, ad_set_id, ad_id, report_date, timezone, currency, spend, impressions, reported_clicks | Existing Meta pipeline |
| Optional mock CPA | conversion_id, referral mapping, mock status, mock commission, event_at_utc | Telegram Experiment 6 mock affiliate adapter |

Keep personally identifying Telegram fields out of campaign-level exports. Store only the minimum linkage necessary for the test lab.

## Manual acceptance walkthrough

1. Seed two clearly labeled mock campaigns and their mock insights; ensure different ad IDs and known daily spend.
2. Issue a campaign-tagged bot deep link for one selected ad.
3. Open the link as a real Telegram test user, press Start, and request admission to the private test channel.
4. Approve through the existing flow and verify that Telegram confirms membership.
5. Confirm exactly one attributed bot start and one verified join under the selected mock campaign, including after app restart and event replay.
6. Open the unified dashboard, verify campaign hierarchy and funnel totals against database records, then export the report.
7. Repeat with an untagged user and an invalid token; confirm they are not assigned a guessed campaign.
8. Simulate a Meta sync failure and delayed Telegram event; verify freshness warnings and successful reconciliation.

## Definition of done

- [ ] Existing Meta and Telegram modules are reused rather than rebuilt.
- [ ] Campaign IDs and referral mappings are stable and auditable.
- [ ] Real Telegram test events appear correctly against mock campaign data.
- [ ] Unified dashboard and export reconcile with stored records.
- [ ] Source/provenance labels prevent false claims of Meta-verified user-level attribution.
- [ ] Mock affiliate events, if enabled, are labeled as simulated.
- [ ] Privacy, error, replay and reconciliation tests pass.
- [ ] README, test instructions and experiment implementation log are complete.

## IDE-agent handoff and execution rules

Follow `TELEGRAM_PROJECT_WORKFLOW.md`'s guidance-first method, adapted for the Meta lab:

1. Inspect current repositories and experiment artifacts before proposing edits. Confirm actual paths and schemas; do not assume the suggested layout exists.
2. Work on **one small task at a time**. Name tasks `m6.f1.<feature_name>`, `m6.f2.<feature_name>`, etc. For larger features, break implementation into internal steps while retaining one feature commit.
3. Explain the current task, why it exists, the rough flow, the exact files to open and only the code needed for the present step.
4. The student writes code, installs packages and runs services unless they explicitly ask the agent to act.
5. Verify each completed task with appropriate tests, diff review and `git status --short`. Review comments for useful business-rule explanations before committing.
6. Give explicit Git staging paths; never use `git add .`. The student commits and pushes after verification.
7. After each commit, update `docs/implementation-log/m6-implementation-log.md` outside the app repo if following the established workspace convention. Include commit hash, files, purpose, concepts learned, code meaning and how to retest.
8. Wait for the student's approval before moving to the next feature or milestone. Never trigger real advertising spend or change a live campaign as part of this experiment.

**First proposed task:** `m6.f1.inspect_existing_data_contracts` — inventory the existing Meta campaign IDs, Telegram referral tables, event schemas and reporting timezones. Do not create new integration tables until this inventory is verified.
