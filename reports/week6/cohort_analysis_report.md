# Week 6 — Customer Cohort and Exploratory Value Analysis

## Scope
- Source: supplied sales transaction sample
- Valid non-returned transactions: 903
- Customers represented: 200
- Observation period: 2024-07-02 to 2026-06-28
- Cohort assignment: month of first observed non-returned transaction

## Method
- Monthly retention counts distinct customers with a non-returned transaction.
- Retention percentage uses the original cohort size as denominator.
- Monthly revenue is discounted transaction value from non-returned records.
- Observed revenue per cohort customer is cumulative observed revenue divided by original cohort size.

## Important interpretation
These are historical observations from the supplied general sales sample.
Observed revenue per customer is not predicted lifetime value.
It is not confirmed insurance premium, commission, or policyholder CLV.
Cohorts have different observation windows; newer cohorts have had less time to generate activity.
No future revenue has been forecast or extrapolated.

## Outputs
- cohort_retention_pct.csv
- cohort_monthly_revenue_inr.csv
- cohort_summary.csv
- cohort_retention_heatmap.png
- cohort_revenue_per_customer.png
