# Week 6 — RFM, Cohort and Customer Value Analysis

## 1. Executive Summary

- Customer sample: **200** profiles.
- RFM eligible customers: **200**.
- Valid non-returned sales transactions: **903**.
- Five-cluster silhouette: **0.3179** (31.79%).
- Best tested clustering result: **k=2**, silhouette **0.3477** (34.77%).
- Observed non-returned discounted sales: **₹7,200,464.20**.

The analysis provides a sample-level view of customer purchasing patterns. It does not establish insurance policyholder lifetime value.

## 2. RFM Methodology

- Recency: days since the latest non-returned transaction.
- Frequency: distinct non-returned sales transactions.
- Monetary: discounted value of non-returned transactions.
- Observation date: 29 June 2026.
- RFM features were log-transformed and standardized before K-Means.

## 3. Customer Segments and Suggested Experiments

| Segment | Customers | Avg Recency (days) | Avg Frequency | Avg Monetary (₹) | Churn Rate |
|---:|---:|---:|---:|---:|---:|
| 0 | 36 | 26.6 | 4.81 | 38,911.82 | 8.33% |
| 1 | 75 | 185.3 | 5.00 | 43,837.18 | 1.33% |
| 2 | 39 | 206.3 | 3.97 | 38,005.26 | 5.13% |
| 3 | 13 | 158.3 | 2.85 | 19,978.38 | 0.00% |
| 4 | 37 | 119.6 | 4.41 | 20,808.81 | 0.00% |

### Provisional segment interpretation

- **Segment 0 — Recently Active, Higher Spending:** Test relevant cross-sell and repeat-purchase engagement; validate the recorded churn indicator.
- **Segment 1 — High Spending, At-Risk of Inactivity:** Prioritize personalized re-engagement and investigate the long gap since the last recorded purchase.
- **Segment 2 — High Spending, Lapsed:** Test win-back communication and investigate reasons for inactivity.
- **Segment 3 — Lower Spending, Lower Frequency:** Explore low-cost education and suitable entry-level offerings; validate customer needs first.
- **Segment 4 — Moderate Spending, Recently Active:** Test relevant product education and cross-sell opportunities.

These are hypotheses for business testing, not proven customer preferences or causal effects. Segment churn rates use the supplied profile-level Churned field.

## 4. Clustering Evaluation

- Requested business segmentation: 5 clusters; silhouette 31.79%.
- Best tested alternative: 2 clusters; silhouette 34.77%.
- The 85% acceptance target was not met.
- The five-cluster output is retained to support the requested five-group business analysis, but cluster separation is modest.
- Silhouette measures cluster separation and cohesion; it is not model prediction accuracy.

## 5. Cohort Retention

- First-observed-purchase cohorts: 16.
- Total cohort customers: 200.
- Mean Month 1 retention across cohorts with an observed Month 1: 16.88%.
- Zero-activity months within an observed cohort window are represented as 0%; months beyond the observation window remain blank.
- Retention is based on at least one non-returned transaction in a month.

Cohorts have unequal observation windows. Newer cohorts must not be compared with older cohorts as if they had equal follow-up time.

## 6. Historical Observed Customer Value

- Highest observed revenue per original cohort customer: 2025-08 — ₹48,990.62 across 3 customers.
- Lowest observed revenue per original cohort customer: 2026-01 — ₹18,111.45 across 1 customer.
- Total observed non-returned discounted sales: ₹7,200,464.20.

These are historical transaction values, not forecasts or customer lifetime value estimates. Cohort size and observation duration differ.

## 7. Business Recommendations

1. Validate the five segment profiles with business stakeholders before using them for customer campaigns.
2. Test re-engagement experiments on customers with high recency values.
3. Test relevant cross-sell and repeat-purchase experiments for recently active customers.
4. Measure campaign response, conversion, incremental contribution and retention using a control group.
5. Obtain verified insurance policy, premium, commission, renewal, cancellation and acquisition-cost data before building an insurance CLV model.

## 8. Data Limitations and Acceptance Gaps

- Cynaris confirmed that the supplied 200 customer profiles are the intended project sample; 50,000+ refers to the production scale the methodology should support.
- General retail sales values are exploratory proxies for historical customer value and purchasing behaviour, not actual insurance policy transactions.
- Profile-level Total_Orders and Total_Revenue do not reconcile with transaction-level sales; RFM therefore uses transaction-derived metrics.
- 42 customer profiles have first-purchase dates later than last-purchase dates; original dates were not silently altered.
- Fintech user IDs have no verified mapping to customer profile IDs and were excluded from customer-level RFM and cohort calculations.
- No verified future CLV target or insurance commission outcome is available. Transaction values, product categories and segments are proxies only, not actual insurance premiums, commissions or predicted insurance CLV.
- Five-cluster silhouette is below the stated 85% target.

### Scalability to 50,000+ Policyholders

The current analysis uses the complete supplied sample of 200 customer profiles and 1,000 sales transactions. The methodology can be extended by:

1. Reusing data validation and cleaning on larger datasets.
2. Using stable customer and policy identifiers for reliable joins.
3. Processing customer and transaction features in batches.
4. Re-evaluating clustering and segment stability at production scale.
5. Incorporating verified premiums, commissions, renewals and acquisition costs when available.
6. Testing predictive models against suitable historical outcomes.

Production-scale performance on 50,000+ records has not yet been benchmarked.

## 9. Deliverables

- `rfm_customer_metrics.csv`
- `customer_segments.csv`
- `segment_profiles.csv`
- `cluster_evaluation.json`
- `rfm_analysis_report.md`
- `cohort_retention_pct.csv`
- `cohort_monthly_revenue_inr.csv`
- `cohort_summary.csv`
- `cohort_analysis_report.md`
- `silhouette_evaluation.png`
- `segment_distribution.png`
- `rfm_distributions.png`
- `cohort_retention_heatmap.png`
- `cohort_revenue_per_customer.png`

## Conclusion

Week 6 establishes reproducible sample-level RFM and cohort analyses. The results provide sample-level RFM and cohort insights using the intended Cynaris sample. Proxy measures do not establish actual insurance CLV. The five-cluster silhouette remains approximately 0.318, below the stated 0.85 target. Performance on 50,000+ policyholders remains to be tested.
