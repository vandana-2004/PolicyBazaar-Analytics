# Week 9 - Dashboard v1

## Project data
Cynaris confirmed that the supplied datasets are the intended project data:
- Customer profiles: 200 records
- Sales transactions: 1,000 records
- Fintech transactions: 800 records

Fintech records are not joined to customer profiles because verified ID mapping is unavailable.

## KPIs
- Customers: 200
- Sales transactions: 1,000
- Valid non-returned transactions: 903
- Observed discounted sales: INR 7,200,464.20
- Customer segments: 5

## Proxy assumptions
Transaction values are historical customer-value proxies. Product categories and RFM segments are exploratory indicators of purchasing behaviour. They are not actual insurance premiums, commissions, claims, renewals or predicted insurance CLV.

## Methodology
Excluded returned transactions, calculated discounted sales, reused Week 6 RFM segments, and aggregated results by segment, month, category and cohort.

## Validation
Segment totals reconcile with dashboard KPIs. Aggregate files passed the customer and transaction identifier text check.

## Scalability to 50,000+ policyholders
The methodology is designed to extend through stable identifiers, repeatable data validation, batch or scheduled processing, and production-scale model evaluation. Performance at that scale has not yet been benchmarked.

## Limitations
The five-cluster silhouette score is approximately 0.318, below the stated 0.85 target. Historical monetary value is not predictive CLV. Insurance-specific outcomes require verified insurance data.

## Peer review
Pending genuine peer feedback.
