# Meta Ads Practical Lab — Experiment 5: Campaign Analytics & Automation

**Status:** Ready for hands-on implementation  
**Prerequisite:** Experiment 4 — Python Campaign Data Pipeline  
**Stack:** Python, SQLite, pandas, Streamlit, pytest; Meta Marketing API (optional, authorized access)  
**Mode:** Guidance-first; implement and verify one small task at a time.

## Objective
Turn the validated campaign dataset from Experiment 4 into a usable analytics dashboard, reproducible reports, and a rule-based automation prototype. Learn to distinguish descriptive metrics from actionable decisions, test automation against mock data, and introduce explicit safeguards before any authorized live campaign change.

## Scope
**In:** KPI definitions, interactive reporting, trend and comparison views, scheduled report generation, configurable rule evaluation, dry-run recommendations, approval gates, audit trails, tests, and optional tightly scoped live API actions.  
**Out:** Launching paid campaigns, autonomous budget increases, ML optimization, individual-user attribution, Telegram joins, broker conversions and CPA revenue. Cross-platform attribution belongs to Experiment 6.

## Implementation milestones

### M5.1 — KPI contracts and analytics foundation
**Goal:** Establish correct, reproducible campaign measurements before creating charts.

Tasks:
- Reuse Experiment 4's campaign, ad-set, ad and daily-insights tables; do not build a second ingestion pipeline.
- Define the reporting grain, account time zone, currency, date range, campaign hierarchy, attribution settings and metric availability.
- Implement tested calculations for spend, impressions, clicks, CTR, CPC, CPM and available Meta-reported results/cost per result.
- Specify safe division, missing values, zero denominators and currency handling. Never silently treat unavailable conversions as zero.
- Create fixture scenarios for a healthy campaign, high-cost campaign, zero-delivery campaign, sparse data and revised historical insights.

Acceptance criteria:
- KPI calculations match independently checked fixture expectations.
- Each displayed metric identifies its source, formula and reporting scope.
- Missing and non-comparable metrics are clearly labeled rather than fabricated.

### M5.2 — Interactive campaign dashboard
**Goal:** Explore advertising performance across accounts, campaigns, ad sets and ads.

Tasks:
- Build a local Streamlit dashboard reading the Experiment 4 database through a dedicated query/service layer.
- Add date-range, campaign, ad-set and ad filters; show reporting time zone and currency.
- Display KPI summaries, daily spend and delivery trends, performance tables and campaign-level comparisons.
- Add drill-down navigation from campaign to ad set to ad, without incorrectly summing pre-aggregated rates.
- Provide empty-state, stale-data and ingestion-error indicators; show the most recent successful sync time.

Acceptance criteria:
- Filters produce correct, consistent totals across KPI cards, charts and tables.
- The dashboard runs entirely from mock fixtures without Meta credentials or advertising spend.
- An empty or partially populated database does not crash the interface.

### M5.3 — Performance analysis and automated reporting
**Goal:** Generate useful, reproducible reports without mistaking correlation for causation.

Tasks:
- Implement date-over-date comparisons with explicit comparison windows and minimum-data checks.
- Compare campaigns using comparable objectives, currencies, attribution settings and date ranges; flag incompatible comparisons.
- Produce a daily or weekly CSV/Markdown summary with metric changes, data freshness, anomalies and caveats.
- Implement a locally invoked report command; optionally add an OS scheduler after the manual run is verified.
- Document that draft campaigns and mock data do not provide evidence of actual ad delivery or performance.

Acceptance criteria:
- Re-running the same report against unchanged data produces identical metrics.
- Reports show their exact date range, data source, attribution context and generation time.
- Missing or late-arriving insights do not produce misleading improvement or decline claims.

### M5.4 — Rule-based automation with dry-run mode
**Goal:** Learn the decision-and-action pipeline without risking accidental campaign changes.

Tasks:
- Define a small, configurable ruleset using explicit thresholds, minimum impressions/spend, lookback windows and cooldown periods.
- Implement a rule evaluator that outputs **observations and proposed actions**, not immediate API writes.
- Support examples such as 'flag unusually high CPC', 'flag zero delivery' and 'propose review of a campaign that crosses a user-defined spend threshold'.
- Implement a dry-run mode that records the proposed action, supporting measurements, timestamp and rule version.
- Add a separate approval gate. Keep write-capable API methods disabled by default; if live action testing is explicitly approved, require authorized permissions, an allowlisted campaign, a strict action allowlist and an independently configured spend-change cap.
- Do not enable autonomous budget increases or live campaign creation in this lab.

Acceptance criteria:
- The engine can evaluate mock fixtures and generate understandable proposals without making network write requests.
- Repeated evaluations honor cooldowns and do not duplicate an already pending action.
- No live mutation occurs without an explicit approval and the required access controls.

### M5.5 — Auditability, reliability and final verification
**Goal:** Confirm that analytics and automation remain accurate and controllable under failure.

Tasks:
- Store rule evaluations, proposed actions, approvals/rejections, attempted executions and outcomes in an audit table.
- Test stale insights, missing permissions, API rate limits, expired tokens, duplicate requests, partial failures and changed campaign state between proposal and execution.
- Where live write testing is authorized, re-fetch the target's current state immediately before applying an approved, allowlisted change; otherwise keep execution mocked.
- Add a manual kill switch for all write operations and ensure failures never trigger automatic spend-increasing retries.
- Run dashboard/report consistency checks and review that logs, screenshots and exports contain no access tokens or unnecessary personal data.
- Document setup, commands, limitations and how to return the system to read-only mode.

Acceptance criteria:
- All mock-mode tests pass without credentials.
- The audit trail reconstructs why each action was proposed and whether it was executed.
- A failed or unauthorized action leaves the advertising account unchanged.
- The project is ready to supply campaign-side metrics to Experiment 6.

## Suggested project structure
```text
meta-ads-lab/
  experiment-05/
    src/
      config.py
      metrics.py
      queries.py
      dashboard.py
      reports.py
      rules.py
      approvals.py
      audit.py
      cli.py
    tests/
      fixtures/
      test_metrics.py
      test_queries.py
      test_reports.py
      test_rules.py
      test_approvals.py
    config/
      rules.example.yaml
    .env.example
    .gitignore
    requirements.txt
    README.md
```

## Data and security boundaries
- Reuse Experiment 4's normalized data and preserve source IDs as strings.
- Keep account currencies separate unless an explicit, dated FX conversion source is introduced.
- Distinguish Meta-reported actions from verified off-platform conversions; the latter are not available in this experiment.
- Mock mode must require no access token. Store any live credentials outside Git and never log authorization headers.
- Use read-only access by default. Live changes are optional, separately approved and limited to an allowlist; never infer approval from a dashboard click that merely previews a proposal.
- Do not use this lab to bypass financial-advertising policies or target-country regulatory requirements.

## Manual verification checklist
- [ ] KPI formulas match fixture calculations.
- [ ] Dashboard totals agree with source rows for the same filters and reporting grain.
- [ ] Zero-delivery and missing-metric scenarios display correctly.
- [ ] Date comparisons use explicit, comparable windows.
- [ ] Report export is reproducible and identifies data freshness.
- [ ] Dry-run rules produce proposals but no live write calls.
- [ ] Duplicate proposals and cooldown behavior are tested.
- [ ] Approval and audit history can be inspected.
- [ ] A kill switch blocks all write-capable operations.
- [ ] All mock-mode tests pass with no Meta account or advertising spend.

## IDE-agent handoff
Follow the master project workflow: guidance-first, one small task at a time. For each task, explain its purpose and rough flow, identify the exact file to open, provide only the current code chunk and wait for the student to implement it. Verify changed files and relevant tests before proposing a commit. Use explicit `git add` paths, never `git add .`; the student commits unless explicitly delegating. After each commit, update `docs/implementation-log/m5-implementation-log.md` with what changed, why it matters, concepts learned, tests and the commit hash. Do not advance before verification.

Suggested task IDs: `m5.f1.kpi_contracts`, `m5.f2.metrics_service`, `m5.f3.dashboard_setup`, `m5.f4.dashboard_filters`, `m5.f5.performance_reports`, `m5.f6.rule_engine`, `m5.f7.dry_run_and_approvals`, `m5.f8.audit_and_reliability`.

## Definition of done
A reproducible local dashboard and reporting workflow analyze Experiment 4's campaign data; a tested rule engine generates auditable, dry-run proposals with explicit approval and safety controls. No paid advertising or live campaign mutation is required to complete this experiment.

**Next:** Experiment 6 — Meta → Telegram Integration.
