# Meta Ads Practical Lab — Experiment 4: Python Campaign Data Pipeline

**Status:** Ready for hands-on implementation  
**Prerequisite:** Experiment 3 — Marketing API Fundamentals  
**Stack:** Python, Meta Marketing API, SQLite (initially), pytest  
**Mode:** Guidance-first; implement one task at a time and verify before continuing.

## Objective
Build a reliable, read-only ingestion pipeline that retrieves authorized Meta Ads campaign structure and performance data, validates and normalizes responses, and persists them for subsequent analytics. Support a mock-data mode so the complete pipeline can be tested without active ad spend or live API access.

## Scope
**In:** API extraction, incremental date-window fetching, pagination, validation, schema normalization, SQLite persistence, retries, observability, mock fixtures, and reconciliation.

**Out:** Campaign creation or modification, live spending, automated optimization, Telegram attribution joins, broker conversions, production deployment, and ML. These belong to later experiments or separate projects.

## Implementation milestones

### M4.1 — Project setup and data contracts
**Goal:** Establish a minimal ingestion project and define its inputs and outputs before writing extraction code.

Tasks:
- Create a dedicated Python environment and install only necessary dependencies.
- Configure environment variables for account ID, API version, access token, database path and mock/live mode. Keep credentials out of Git.
- Define typed records for campaign, ad set, ad and daily insights. Keep stable Meta IDs as strings.
- Define metric conventions: reporting date, account time zone, currency, attribution settings, action breakdowns, and nullable metrics. Do not infer missing values as zero.
- Create versioned mock API response fixtures, including empty and malformed examples.

Acceptance:
- App starts in mock mode with no credentials.
- Configuration validation fails clearly for incomplete live-mode settings.
- Data contracts and mock fixtures are documented and tested.

### M4.2 — Read-only extraction client
**Goal:** Retrieve authorized account structure and daily performance records.

Tasks:
- Build a small API client with explicit read-only methods for campaigns, ad sets, ads and insights.
- Request only required fields and capture the requested reporting window and level.
- Implement pagination until all pages are retrieved, with a maximum-page guard for testing.
- Handle HTTP errors, Meta API errors, unavailable permissions and expired tokens without exposing secrets.
- Support fixture-backed mock responses through the same client interface.

Acceptance:
- A complete paginated mock dataset is retrieved exactly once per page.
- Read-only live requests work when the account and permissions are available.
- Authentication and permission failures produce actionable, sanitized errors.

### M4.3 — Normalization and persistence
**Goal:** Convert nested API responses into consistent, queryable database records.

Tasks:
- Normalize campaign hierarchy and daily insights into separate tables.
- Store monetary values with explicit currency and documented unit handling; avoid binary floating-point for financial totals.
- Preserve original source IDs, ingestion timestamps, reporting windows and API version.
- Create database constraints and idempotent upserts for re-runs.
- Retain raw, sanitized response fixtures or optional raw payload archives for debugging without storing access tokens.

Acceptance:
- The same input can be ingested twice without duplicate logical records.
- Missing optional metrics and empty result sets are handled correctly.
- Relationships between ads, ad sets and campaigns remain intact.

### M4.4 — Incremental ingestion and reliability
**Goal:** Run repeatable date-scoped imports and recover safely from transient failures.

Tasks:
- Implement CLI commands for initial backfill and incremental date-window sync.
- Persist sync checkpoints only after successful writes; allow a failed window to be retried.
- Use bounded retries with backoff for retryable errors, respecting any rate-limit guidance; fail fast on permission errors.
- Log run IDs, requested windows, page counts, inserted/updated rows, duration and sanitized errors.
- Add a configurable recent-day refresh window to accommodate delayed or revised reporting.

Acceptance:
- Interrupted runs can resume without losing or duplicating records.
- Retry behavior is tested with mocked failures.
- A run summary distinguishes completed, partial and failed imports.

### M4.5 — Quality checks and handoff
**Goal:** Confirm that the local dataset is suitable for Experiment 5 analytics.

Tasks:
- Add tests for pagination, missing fields, duplicate pages, rate limits, schema drift and partial writes.
- Reconcile imported totals against the same date range, level, time zone and attribution settings in Ads Manager when live data is available.
- Document differences between mock results and real account data, including API permissions and reporting limitations.
- Export a simple daily campaign-level report as CSV for downstream dashboard work.
- Write a README with mock-mode setup, live-mode prerequisites, commands, security notes and known limitations.

Acceptance:
- Automated tests pass in mock mode without a Meta account.
- CSV export contains one row per defined campaign/date/account reporting grain.
- Reconciliation findings and any unresolved differences are documented.

## Suggested project structure
```text
meta-ads-lab/
  experiment-04/
    src/
      config.py
      api_client.py
      models.py
      normalize.py
      storage.py
      pipeline.py
      cli.py
    tests/
      fixtures/
      test_api_client.py
      test_normalize.py
      test_pipeline.py
    .env.example
    .gitignore
    requirements.txt
    README.md
```

## Security and reporting boundaries
- Never commit API tokens, raw authorization headers or user-level personal information.
- Use only ad accounts the user is authorized to access.
- Treat insights as aggregate advertising measurements; do not assume they identify individual Telegram users.
- Distinguish unavailable metrics, zero-valued metrics and metrics with different attribution settings.
- No write-capable Marketing API operations in this experiment.

## Manual verification checklist
- [ ] Mock mode runs without Meta credentials.
- [ ] Multi-page responses are fully ingested.
- [ ] Empty windows produce a successful zero-row run.
- [ ] Duplicate imports do not create duplicate logical records.
- [ ] A transient error is retried and a permanent permission error is not.
- [ ] Failed runs do not advance the successful checkpoint.
- [ ] CSV daily totals match the stored records.
- [ ] Live account totals are reconciled where access is available.
- [ ] No credentials or sensitive data appear in logs or commits.

## IDE-agent handoff
Follow the master project workflow: guidance-first, one small task at a time. For each task, explain the purpose and rough flow, identify the exact file, give only the current code chunk, and wait for the student to implement and run it. Verify changed files and relevant tests before proposing a commit. Use explicit `git add` paths, never `git add .`; the student performs commits unless explicitly delegating. After each commit, update `docs/implementation-log/m4-implementation-log.md` with what changed, why, concepts learned, commands/tests and the commit hash. Do not advance to the next task before verification.

Suggested task IDs: `m4.f1.project_setup`, `m4.f2.data_contracts`, `m4.f3.api_client`, `m4.f4.pagination`, `m4.f5.normalization`, `m4.f6.persistence`, `m4.f7.incremental_sync`, `m4.f8.reliability`, `m4.f9.reconciliation`.

## Definition of done
A reproducible, tested, read-only Python pipeline imports mock or authorized live Meta campaign data into SQLite, safely supports re-runs and incremental sync, and exports daily campaign metrics for Experiment 5.

**Next:** Experiment 5 — Campaign Analytics & Automation.
