# Agent Handoff — Meta Ads Practical Lab

Use this as the durable resume entry point. Keep detailed feature history in the experiment implementation logs rather than here.

## Resume protocol

Before proposing work:

1. If a repository exists, inspect `git status --short` and `git log --oneline -5`.
2. Read `docs/META_PROJECT_WORKFLOW.md` (or its actual checked-in path).
3. Read the active experiment planner and matching implementation log.
4. Inspect relevant existing code, authorized API setup or the student's current Ads Manager state before assuming anything is configured.
5. Identify the next *unfinished* acceptance criterion and propose only its first small action.

The workflow governs **how** to work; the active planner governs **what** to build; the log documents what has actually been verified.

## Current checkpoint

**Active work:** Experiment 3, Marketing API Fundamentals. The student chose to move from Ads Manager orientation to application/API work. Experiment 1's final draft and no-spend verification remain open; Experiment 2 was deferred, not completed. Read `docs/implementation-log/m3-implementation-log.md` for task evidence and limitations.

The student reports that a Meta developer app and Graph API Explorer are available at `v26.0`, and that `ads_read` allowed an account-list request. `src/inspect_accounts.py` returned one account on its first page with no further page. The campaign-list request returned an empty `data` list in Explorer, and `src/inspect_campaign.py` returned zero campaigns with no next page. `src/inspect_adsets.py` returned zero ad sets with no next page, and `src/inspect_ads.py` returned zero ads with no next page. The account-level Insights request for September 1-26, 2026 returned an empty `data` list in Explorer and zero rows with no next page from `src/inspect_insights.py`. These are student-reported runs; the agent did not run live requests. No token or raw account response was shared.

**Repository:** `C:\Users\alaud\OneDrive\Desktop\meta-camp` is on `main` at commit `2e7223c` and tracks `origin/main`. `origin` is configured as the student-provided `https://github.com/git4alauddin/meta-campaign-lab.git`; live remote contents have not been fetched by the agent. `.env` is ignored and must never be inspected or staged. By agreement, a commit's hash is recorded in the implementation log with the next feature commit; no hash-only commit is made.

Synthetic Experiment 3 fixtures now exist in `tests/fixtures/` for four campaigns, five ad sets, five ads, account/campaign/ad-set/ad aggregate Insights, seven days of account and campaign trends, two-page pagination, missing/zero/empty metrics, and illustrative API errors. The agent validated JSON syntax, synthetic markers, parent IDs, and aggregate and per-day additive totals. `src/inspect_insights.py` consumes aggregate Insights fixtures by default and normalizes their rows; the student reports that both the fixture and live account-level modes worked after regenerating the token. `src/inspect_campaign.py` now defaults to synthetic pages and collects all four campaigns from both fixtures, with an explicit `--source live` mode. Eleven offline tests passed across Insights and campaign pagination, including a mocked two-page live campaign request. The agent made no live Meta request and did not inspect `.env`.

## Planned experiment sequence

1. Ads Manager Fundamentals — `meta-experiment-01-ads-manager-fundamentals.md`
2. Campaign Design & Testing — `meta-experiment-02-campaign-design-testing.md`
3. Marketing API Fundamentals — `meta-experiment-03-marketing-api-fundamentals.md`
4. Python Campaign Data Pipeline — `meta-experiment-04-python-campaign-data-pipeline.md`
5. Campaign Analytics & Automation — `meta-experiment-05-campaign-analytics-automation.md`
6. Meta → Telegram Integration — `meta-experiment-06-meta-telegram-integration.md`

## Working contract

- Guidance-first, one independently verifiable task at a time. Student performs GUI steps, writes/runs code and executes Git commands unless explicitly delegating.
- The student explicitly requires an instruction before the agent writes code to a file or runs a commit. A request for the next step alone does not authorize either action.
- Explain purpose, rough flow, exact UI location/files, first step and verification. Do not dump a full milestone implementation.
- Verify actual evidence before claiming completion. Ask for redacted screenshots or command output when the agent cannot inspect the state directly.
- After verification, provide a PowerShell commit block with explicit reviewed paths when code/docs were changed. Never use `git add .`; never commit/push automatically.
- Update the matching implementation log. `Commit: Pending` is acceptable until a real hash is available; use `N/A` for non-repository GUI tasks.
- Keep credentials private: never request raw access tokens, inspect `.env`, paste sensitive API responses or expose ad-account personal details.
- Never publish ads, authorize expenditure, modify production campaigns or escalate permissions without the student's explicit approval.

## Important boundaries

- Experiments 1–2 are GUI-first and unpublished; use a non-financial sample business.
- Experiment 3 begins read-only. API access and data availability depend on the actual account, permissions and current Meta policies.
- Experiments 4–5 must distinguish sample fixtures from actual Meta Insights and reconcile metric definitions, time zones, currency and attribution windows. Any automation starts in dry-run mode.
- Experiment 6 links campaign metadata to Telegram referrals; Meta does not automatically identify the Telegram member who clicked an ad. Record unknown attribution honestly and reuse the existing Telegram lab rather than reimplementing it.
- Live Forex affiliate promotions, broker integration and real conversion postbacks require separate authorization, policy/legal review and explicit scope.

## Feature loop

1. Read active planner and log; inspect current state.
2. Propose `mX.fY.feature_name` and only its first small action.
3. Student performs the action; agent explains unfamiliar concepts as needed.
4. Verify settings, tests, API output or observed behavior; inspect diff and Git status when relevant.
5. Review security/readability; student commits reviewed paths if applicable.
6. Update the log with evidence and actual commit hash or `Pending`/`N/A`.
7. Ask before starting the next experiment.

## Updating this handoff

Change only durable resume information: current experiment checkpoint, verified project/repo paths, major source-of-truth changes and stable collaboration rules. Never guess a local project path or copy the Telegram project's local path/GitHub remote into this new Meta project without confirmation.

**Next agent action:** Ask the student to run `src/inspect_campaign.py` in PyCharm without parameters and verify two synthetic pages and four campaigns. After that, provide a student-run commit block for `m3.f10.campaign_pagination`. Continue Experiment 3 reliability work one small task at a time. Do not create or publish an ad or initiate spending.
