# Meta Ads Practical Lab — Experiment 1: Ads Manager Fundamentals

**Status:** Ready for hands-on implementation  
**Mode:** GUI-first, guidance-first, one verified task at a time  
**Cost boundary:** No paid campaign launch or spending in this experiment.

## Objective
Learn the real Meta Ads Manager workflow by configuring an advertising workspace and building a complete **draft** campaign, ad set, and ad. Understand which settings live at each level and how to inspect the draft before publishing.

## Prerequisites
- A Facebook account with legitimate access to an appropriate Meta business portfolio and ad account.
- Access to Meta Ads Manager; some setup steps may require identity, business or payment verification depending on the account and region.
- A safe, non-financial sample product or service for practice. Do **not** publish a forex or broker advertisement as part of this experiment.
- A local folder for screenshots, observations and an implementation log. Redact account IDs, tokens, payment details and personal information from shared screenshots.

## Scope
**In:** account orientation; campaign/ad set/ad hierarchy; draft objective and settings; sample audience, placements, budget and creative; review and inspection; learning notes.  
**Out:** publishing, paid delivery, real performance optimization, Marketing API, Telegram integration, Pixel/CAPI deployment and financial-advertising approvals.

## Milestones

### M1.1 — Workspace and Account Orientation
**Tasks**
1. Open Meta Ads Manager and identify the correct business portfolio and ad account.
2. Inspect account currency, timezone, account status, permissions and billing/settings areas without changing sensitive settings unnecessarily.
3. Locate Campaigns, Ad sets, Ads, reporting columns and draft controls.
4. Draw a simple campaign → ad set → ad hierarchy and note the purpose of each level.

**Acceptance criteria**
- Correct accessible ad account identified.
- Can navigate among the three hierarchy levels and distinguish their responsibilities.
- No unintended spending, publication or account-setting changes.

### M1.2 — Create a Draft Campaign
**Tasks**
1. Choose a harmless sample business goal and map it to an available Ads Manager campaign objective.
2. Start a new campaign; give it a consistent experiment name, such as `lab01_sample_draft`.
3. Inspect objective-specific settings and identify any campaign-level budget or automated options shown.
4. Save as a draft. Do not publish.

**Acceptance criteria**
- Draft campaign exists with a documented objective and reason for choosing it.
- Can identify which settings are controlled at campaign level.
- Campaign remains unpublished.

### M1.3 — Configure a Draft Ad Set
**Tasks**
1. Configure the destination/conversion location supported by the chosen objective; use a safe practice destination.
2. Explore audience controls, geography, placements, schedule and budget settings actually available to the account.
3. Record which settings are manual and which are automated or Advantage+ controlled.
4. Estimate theoretical spend from the configured budget and duration; do not start delivery.

**Acceptance criteria**
- Draft ad set is internally consistent with the campaign objective.
- Can explain targeting, placement, schedule and budget choices.
- No audience or targeting claims based on unavailable controls.

### M1.4 — Build a Draft Ad
**Tasks**
1. Select an authorized page/identity if required.
2. Prepare original or properly licensed sample creative and compliant, non-financial practice copy.
3. Add an appropriate call to action and safe destination; inspect available tracking fields without activating new integrations.
4. Preview the ad in available placements and check formatting, links and disclosures.

**Acceptance criteria**
- Draft ad has a coherent identity, creative, copy, CTA and destination.
- Preview checked for major placements offered by the account.
- No misleading claims, unlicensed assets or publication.

### M1.5 — Review, Document and Verify
**Tasks**
1. Review the campaign → ad set → ad configuration from top to bottom.
2. Identify warnings, incomplete fields and any settings that would need attention before a future launch.
3. Capture sanitized screenshots and write a short configuration summary.
4. Confirm that all experiment assets remain drafts and that no spend occurred as a result of this lab.
5. Record lessons and questions for Experiment 2.

**Acceptance criteria**
- Complete, inspectable draft hierarchy or documented account restriction preventing a specific step.
- Configuration summary and sanitized evidence saved.
- No accidental publication or spending.

## Execution Workflow for the IDE/Learning Agent
Follow the Telegram project's guidance-first pattern, adapted for GUI work:

1. Present **one small task** within the current milestone, its purpose and expected result.
2. Tell the learner exactly which Ads Manager screen to open and what to inspect or configure.
3. The learner performs all clicks and account actions unless explicitly requesting another form of assistance.
4. Verify using the learner's description or redacted screenshot. Do not assume a setting exists if the interface differs.
5. Record completion and learning notes; only then proceed to the next task.
6. Never instruct the learner to click **Publish**, activate billing or incur ad spend during this experiment.

**Task naming:** `m1.f1.workspace_orientation`, `m1.f2.draft_campaign`, `m1.f3.draft_ad_set`, `m1.f4.draft_ad`, `m1.f5.review_and_verify`.

## Implementation Log Template
For each task record:
- Task ID and status
- What was configured or inspected
- Why the setting matters
- Concepts learned
- Evidence (redacted screenshot or written observation)
- Verification outcome and unresolved issues

If notes are kept in Git, commit each verified task using explicit paths; never commit credentials, billing information or unredacted screenshots. No Git repository is required for the Ads Manager draft itself.

## Definition of Done
Experiment 1 is complete when the learner can independently navigate Ads Manager, explain campaign/ad set/ad responsibilities, configure and inspect a sample draft, identify settings that affect budget and delivery, and verify that nothing was published.

## Handoff to Experiment 2
Experiment 2 will compare campaign objectives, audience configurations, budgets, placements and creative variants through controlled draft exercises and hypothetical test scenarios. Real-money tests, if ever undertaken, require separate explicit approval and applicable policy checks.

## Reference
Official Meta Ads Manager learning resources: https://www.facebookblueprint.com/ and https://www.facebook.com/business/tools/ads-manager . Interface and available options may change by account, region and objective.
