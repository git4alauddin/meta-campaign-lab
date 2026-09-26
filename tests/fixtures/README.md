# Experiment 3 synthetic API fixtures

Every JSON file here is invented for local learning and tests. None contains a response copied from the student's Meta account, a real account/object ID, an access token, or measured advertising performance. The top-level _fixture field marks synthetic test data; it is not a Meta API field. A parser should read data, paging, or error as appropriate and ignore _fixture.

| File | Scenario |
| --- | --- |
| sample_accounts.json | One accessible synthetic ad account |
| sample_campaigns.json | Campaign page 1: two campaigns and a token-free next link |
| sample_campaigns_page_2.json | Campaign page 2: two campaigns and no next link |
| sample_adsets.json | Five ad sets linked to the four campaigns |
| sample_ads.json | Five ads linked to the ad sets and campaigns |
| sample_insights.json | One account-level aggregate row |
| sample_insights_campaign.json | Three campaign-level aggregate rows |
| sample_insights_adset.json | Four ad-set-level aggregate rows |
| sample_insights_ad.json | Four ad-level aggregate rows |
| sample_insights_daily.json | Seven daily account-level rows |
| sample_insights_campaign_daily.json | Twenty-one daily campaign-level rows |
| sample_insights_zero.json | Explicit zero-valued campaign row for a separate test |
| sample_insights_empty.json | Successful Insights response with no rows |
| sample_error_expired_token.json | Illustrative expired-token error body |
| sample_error_permission.json | Illustrative missing-permission error body |
| sample_error_rate_limit.json | Illustrative rate-limit error body |

All aggregates cover September 1-26, 2026. The invented delivery occurs September 20-26, and the daily files cover those seven days. Dates use the synthetic account's America/New_York reporting time zone. The synthetic account uses USD. Spend is represented as a decimal string; impressions, clicks, and reach are integer strings, matching the intended parser inputs.

Two traffic campaigns provide a comparable healthy versus high-cost case. An awareness campaign has a different objective and should not be compared as if it had the same goal. A fourth campaign, ad set, and ad have no aggregate Insights row, representing absent delivery data. That absence is not a reported numeric zero. The separate sample_insights_zero.json contains explicit zeros to test the distinction. One campaign/day row omits reach to test a missing metric.

Campaign, ad-set, and ad IDs deliberately match across files. Spend, impressions, and clicks reconcile across reporting levels and daily rows: 100.00, 14000, and 400 for the full synthetic account window. Do not sum reach across campaigns, ads, or days; it counts unique people within each reporting scope. Derived rates such as CTR, CPC, and CPM should be calculated from additive base metrics for the selected scope.

The invented campaign totals give useful KPI checks:

| Campaign | Spend | Impressions | Clicks | CTR | CPC | CPM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Traffic - Healthy | 25.00 | 5000 | 250 | 5.00% | 0.10 | 5.00 |
| Traffic - High Cost | 60.00 | 3000 | 60 | 2.00% | 1.00 | 20.00 |
| Awareness | 15.00 | 6000 | 90 | 1.50% | 0.1667 | 2.50 |

CTR = clicks / impressions x 100, CPC = spend / clicks, and CPM = spend / impressions x 1000. The CPC shown for Awareness is rounded; calculations should keep full precision until display. These are synthetic expectations, not Meta-reported performance.

The paging URL and cursors are invented and contain no token. Do not send fixture URLs to Meta. Error bodies and HTTP status metadata are illustrative test inputs, not guarantees of Meta's exact error messages or status mappings. A network failure has no JSON response body and needs a simulated transport exception.

These files do not prove live-data parsing, pagination, or error handling. They are inputs for those later checks.
