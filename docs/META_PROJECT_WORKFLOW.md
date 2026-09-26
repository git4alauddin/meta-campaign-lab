# Meta Ads Practical Lab — Project Workflow

**Status:** Ready for hands-on implementation  
**Purpose:** Complete six Meta Ads experiments through guided, independently verified tasks.  
**Authority:** This workflow defines *how* we work. The active experiment planner defines *what* is in scope, including acceptance criteria. Raise conflicts instead of silently changing either.

## 1. Lab map

| Experiment | Planner | Deliverable |
|---|---|---|
| 1 — Ads Manager Fundamentals | `meta-experiment-01-ads-manager-fundamentals.md` | Explore the account and build an unpublished draft campaign |
| 2 — Campaign Design & Testing | `meta-experiment-02-campaign-design-testing.md` | Compare objectives, audiences, budgets, placements, creatives and test designs |
| 3 — Marketing API Fundamentals | `meta-experiment-03-marketing-api-fundamentals.md` | Authorized, initially read-only API access and sample/real responses |
| 4 — Python Campaign Data Pipeline | `meta-experiment-04-python-campaign-data-pipeline.md` | Extract, normalize, validate and persist campaign data |
| 5 — Campaign Analytics & Automation | `meta-experiment-05-campaign-analytics-automation.md` | Dashboard, reporting and guarded dry-run automation |
| 6 — Meta → Telegram Integration | `meta-experiment-06-meta-telegram-integration.md` | Campaign-linked referrals and reconciled acquisition reporting |

Complete experiments in order unless the student approves a change. Reuse verified work; never present mock results as live Meta performance.

## 2. Working rhythm

```text
Read workflow + active planner + implementation log
  → Inspect actual account/repo state
  → Propose ONE small feature and explain why it matters
  → Student performs GUI actions or writes/runs code
  → Agent reviews evidence and verifies acceptance criteria
  → Review readability and security
  → Student commits/pushes relevant code/docs, if any
  → Update the experiment log
  → Proceed only after verification or a documented blocker
```

**Guidance-first:** The student owns Meta UI actions, app configuration, package installation, code execution and Git commands. The agent may inspect files, diffs, status, shared screenshots (with secrets redacted), and command output. Do not edit code, run installs, publish ads, alter budgets, request elevated permissions or commit without explicit delegation. Never publish an ad or initiate expenditure without the student's specific approval for that action.

## 3. Feature naming and task proposal

Use `m<experiment>.f<feature>.<short_name>` consistently in the planner tracker, Git commit title and implementation log. Examples: `m1.f1.ads_account_orientation`, `m3.f2.read_only_token_setup`, `m4.f3.insights_normalization`, `m6.f2.campaign_referral_mapping`. Derive the actual sequence from the active planner, not these examples.

For each feature, provide **what and why**, a brief **rough flow**, the **exact UI section or file(s)**, **one first action**, and **observable verification**. Teach new Meta concepts, Python/API patterns and analytics concepts when encountered; provide code only for the current small step. Ask the student to implement and return with evidence before continuing.

## 4. Experiment-specific execution rules

- **Experiments 1–2 (GUI):** Use a test/non-financial example. Keep configurations as drafts. Verify settings from screenshots or the student's observed UI; do not claim an ad has run. UI labels and available options may vary by account, region and date. Record actual settings and any unavailable options.
- **Experiment 3 (API):** Consult current official Meta documentation for permissions, endpoints and API versions. Begin with minimum required, read-only access. Keep tokens out of chat, source control, logs and screenshots. Do not assume a developer app automatically has production access to every ad account.
- **Experiment 4 (pipeline):** Separate real authorized API responses from fixtures. Validate schema, pagination, retries, rate-limit handling, incremental loads, deduplication and database integrity. Do not invent missing campaign metrics.
- **Experiment 5 (analytics):** Reconcile dashboard values to source data, dates, attribution settings, currency and time zone. Automation is dry-run by default; require explicit approval, access checks, budget limits, audit logs and rollback planning before any real write action.
- **Experiment 6 (integration):** Use campaign-tagged links and Telegram bot referrals. Distinguish clicks, bot starts, join requests and verified memberships. Do not claim Meta provides person-level identities for Telegram joiners. Preserve unknown/unattributed cases and avoid double-counting. Reuse the Telegram lab's verified contracts instead of rewriting it.

## 5. Verification standard

For each task, check the relevant evidence: actual Ads Manager settings, redacted screenshots, API status/response shape, tests, sample fixtures, database records, dashboards and `git diff`/`git status --short`. Never claim an API request, GUI action, live ad delivery or Telegram join was verified unless observed. Record the exact blocker and diagnostic step if verification is impossible.

At each milestone, check every acceptance criterion in the planner. At the end of each experiment, run its end-to-end demonstration and obtain approval before the next experiment.

## 6. Git and implementation logs

Commit each completed and verified code/documentation feature when a repository exists. GUI-only tasks may produce screenshots with secrets/account identifiers redacted and a learning log; do not invent a Git commit when none exists. Stage **explicit reviewed paths**, never `git add .`. Student runs commits and pushes by default.

```powershell
git status --short
git add docs/implementation-log/m3-implementation-log.md app/meta_client.py tests/test_meta_client.py
git commit -m "m3.f2.read_only_token_setup"
git push
```

*Example only: inspect the real repo and use only paths that actually changed.* Never commit `.env`, API tokens, personal data exports, credentials or sensitive screenshots.

Maintain `docs/implementation-log/m1-implementation-log.md` through `m6-implementation-log.md` (adapt to actual repo layout). For each feature record: ID, status, actual commit hash or `Pending`/`N/A`, what changed, why, concepts learned, technology notes, relevant code meaning, exact files/UI settings, verification evidence, reproducible check and open issues. The log is a learning resource, not just a completion checklist.

## 7. Source-of-truth and safety boundaries

1. At resume, inspect Git status and recent commits (if a repo exists), read this workflow, active planner, matching log and relevant code or Ads Manager configuration.
2. Do not assume the suggested repo layout or account configuration already exists. Do not invent permissions, token scopes, account IDs or measured campaign performance.
3. Financial/Forex affiliate advertising is **not** the initial practice campaign. Before any future live financial promotion, separately verify applicable target-market law, broker authorization, Meta advertising policy and data-handling obligations. A working API integration does not imply advertising approval.
4. Do not send unverified or sensitive personal conversion data to Meta. Respect consent and applicable privacy rules for Pixel/Conversions API use.
5. Real ad publishing, financial spend, production API writes and broker integrations remain outside the lab unless explicitly scoped and separately approved.

## 8. Full-lab definition of done

All six planners meet their acceptance criteria; evidence and logs distinguish unpublished drafts, simulated responses, authorized live API data and real Telegram events. Demonstrate an authorized campaign-data extraction → persisted metrics → reconciled dashboard → tagged Telegram referral → verified membership journey, with attribution gaps and privacy constraints documented. Do not claim live financial CPA conversion unless a separately authorized broker integration has actually been implemented and verified.

**First instruction to the IDE agent:** Read `AGENT_HANDOFF.md`, this workflow, Experiment 1's planner and any existing implementation log. Inspect the actual repo/account state. Propose only the first unfinished small step; do not install, edit, publish, spend or commit anything without explicit instruction.
