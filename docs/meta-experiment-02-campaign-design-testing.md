# Meta Ads Practical Lab — Experiment 2: Campaign Design & Testing

**Status:** Ready for hands-on implementation  
**Mode:** GUI-first, guidance-first, one verified task at a time  
**Cost boundary:** No campaign publishing or ad spend.  
**Depends on:** Experiment 1 — Ads Manager Fundamentals.

## Objective
Learn to design, compare and document Meta campaign configurations using a harmless sample product or service. Practice defining measurable objectives, audience hypotheses, budgets, placements, creative variations and controlled tests. This is a **configuration lab**, not a claim about actual campaign performance.

## Prerequisites
- Complete Experiment 1 and have access to the appropriate Meta ad account.
- Use a non-financial sample business for practice; do not use a forex/broker promotion in this lab.
- Keep draft campaigns unpublished. Do not enter payment details or publish without a separate explicit decision.
- Maintain a local experiment log; redact personal information, account identifiers and billing details from shared screenshots.

## Scope
**In:** campaign goal/KPI mapping; draft audience variants; budget/schedule scenarios; placement options; creative hypotheses; A/B-test design; configuration comparison and documentation.  
**Out:** live experiments, claims about real CTR/CPA/ROAS, Marketing API calls, Pixel/CAPI, Telegram integration, broker offers and regulated financial advertising.

## Milestones

### M2.1 — Define Campaign Goals and KPIs
**Tasks**
1. Select one harmless sample business and define one concrete conversion goal (e.g., a demo landing-page visit or sample lead).
2. Compare at least two relevant objectives visible in the current Ads Manager UI. Note that options can differ by account and objective.
3. For each objective, document the desired user action and the metrics that would eventually measure it (e.g., impressions, link clicks, landing-page views or leads, where available).
4. Create or duplicate clearly named unpublished campaign drafts to preserve alternative configurations.

**Acceptance criteria**
- Written goal and objective rationale for each draft.
- KPI definitions distinguish observed metrics from hypothetical targets.
- All variants remain unpublished.

### M2.2 — Audience Strategy Lab
**Tasks**
1. Create a baseline ad-set draft with an appropriate, broad sample audience.
2. Make a second draft changing only one audience dimension that the account/UI permits (such as location, age range or an available targeting option).
3. Inspect estimated audience indicators if provided; record them as platform estimates, not guaranteed reach.
4. Note which audience controls are fixed, suggested or automatically expanded by Meta's current configuration.
5. Document a testable hypothesis and any policy or privacy constraints.

**Acceptance criteria**
- Two documented audience variants with one intentional difference.
- Able to explain why the changed variable might matter without claiming a performance winner.
- No use of sensitive personal traits or unsupported targeting options.

### M2.3 — Budget, Schedule and Placement Scenarios
**Tasks**
1. Inspect campaign-level versus ad-set-level budget controls available for the chosen objective.
2. Compare two hypothetical budget scenarios and record the currency, duration and implied maximum planned spend; do not publish.
3. Inspect schedule, optimization and bid-related settings exposed in the account.
4. Compare automatic placements with a permitted manual-placement draft, if the UI supports both.
5. Record which differences would make a future comparison invalid if changed simultaneously.

**Acceptance criteria**
- A comparison sheet showing budget, duration, placement and optimization assumptions.
- Correct distinction between a configured budget and actual spend.
- No active ads or incurred costs.

### M2.4 — Creative Variations and A/B-Test Design
**Tasks**
1. Produce two compliant sample ad creatives for the same harmless offer, changing one primary element (e.g., headline or image).
2. Inspect supported creative formats, destination URL fields and preview placements in Ads Manager.
3. Build a written A/B-test plan: hypothesis, control, variant, primary metric, secondary diagnostics and conditions to hold constant.
4. Identify minimum practical considerations for a future live test: sufficient delivery, consistent attribution and avoiding premature conclusions.
5. Save creative previews or redacted screenshots where permitted.

**Acceptance criteria**
- Two identifiable creative variants with one controlled difference.
- A written test design that avoids changing audience, budget and creative all at once.
- No unsupported claim that one variant will outperform the other.

### M2.5 — Configuration Review and Experiment Report
**Tasks**
1. Audit all drafts for objective, audience, placements, schedule, budget, creative and destination consistency.
2. Record any Ads Manager warnings or unavailable options exactly as observed; do not bypass restrictions.
3. Prepare a compact comparison table of the variants and the question each would test.
4. Explain which metrics require live delivery and which settings can be inspected without spending.
5. Verify every campaign/ad set/ad remains a draft or otherwise inactive, and capture the final status.

**Acceptance criteria**
- Complete configuration report and evidence of draft/inactive status.
- No live delivery, unexpected charges or unsupported performance conclusions.
- Clear handoff to Experiment 3: Marketing API Fundamentals.

## Suggested Local Documentation
```text
meta-ads-lab/
  docs/
    experiment-02/
      campaign-variants.md
      audience-comparison.md
      budget-placement-scenarios.md
      creative-test-plan.md
      implementation-log.md
      evidence/              # redacted screenshots only
```

No application code or database is required in Experiment 2.

## Manual Verification Checklist
- [ ] Baseline and variant campaigns are identifiable and unpublished.
- [ ] Every comparison identifies the one variable deliberately changed.
- [ ] Hypothetical numbers are labeled as assumptions, not actual results.
- [ ] Objective-specific and automated settings are recorded as observed.
- [ ] Creative previews and destinations are reviewed.
- [ ] Account, billing and personal details are not exposed in logs/screenshots.
- [ ] No live ads, spend or financial-product promotions.

## IDE-Agent / Learning Handoff
Follow the same guidance-first workflow as the Telegram lab:
1. Propose only the current small task, named `m2.fN.descriptive_name`.
2. State its purpose, rough UI flow, exact expected evidence and acceptance criteria.
3. The learner performs UI actions; the agent does not assume access to the Meta account or take publishing/billing actions.
4. Review learner-provided screenshots or observations; ask for redaction where necessary.
5. Verify the current task before moving on. Explain UI differences rather than inventing unavailable controls.
6. Where a local document changes, review the diff and provide an explicit-path Git commit block only after verification; the learner commits and pushes.
7. Update the experiment implementation log with what was configured, why, what was learned and how to reproduce it.
8. Do not proceed to the next milestone until the learner confirms completion.

## Definition of Done
The learner can independently configure and compare draft campaign strategies, describe a controlled creative test, identify the limitations of draft-only analysis, and provide a verified configuration report without spending money.

## Next Experiment
**Experiment 3 — Marketing API Fundamentals:** developer app, permissions, tokens, read-only ad-account discovery and campaign data retrieval. API access and account permissions are not guaranteed merely by completing this GUI lab.
