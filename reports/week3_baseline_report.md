# Week 3 - Baseline Metrics

Generated reproducibly from the supplied raw CSV files.

## Customer Profiles
- Customers: 200
- Average profile revenue: INR 24963.10
- Average orders: 11.54
- Churn rate: 3.00%

## Sales Transactions
- Transactions: 1000
- Gross recorded sales: INR 8456050.00
- Sales after discounts: INR 8021851.20
- Returned records: 97
- Non-returned records: 903
- Non-returned sales after discounts: INR 7200464.20

## Fintech Transactions
- Transactions: 800
- Status counts: {'Failed': 161, 'Pending': 162, 'Success': 477}
- Successful amount: INR 11685052.83
- Fraud-flagged records: 25
- Successful fraud-flagged records: 14

## Data Limitations
- Only 200 customer profiles supplied, not the 50,000 target.
- Fintech user IDs have no verified mapping to Customer_ID.
- Sales data is not confirmed as insurance-policy revenue.
- These baselines are not validated insurance CLV metrics.

## Interpretation
These are initial dataset baselines, not verified insurance revenue or CLV.
Fintech amounts are reported separately because customer ID mapping is unavailable.
Non-returned sales exclude records marked as returned; this is a proxy, not verified net revenue.
