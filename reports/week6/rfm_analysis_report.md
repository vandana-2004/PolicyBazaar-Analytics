# Week 6 — RFM Customer Segmentation

## Scope
- Customer profiles: 200
- Eligible customers: 200
- Excluded customers: 0
- Observation date: 2026-06-29

## RFM Methodology
- Recency: days since last non-returned transaction.
- Frequency: distinct non-returned transactions.
- Monetary: discounted non-returned transaction value.
- Monetary values are not confirmed insurance premiums.
- Features were log-transformed and standardized.

## K-Means Evaluation
- Requested clusters: 5
- Five-cluster silhouette: 0.3179
- Five-cluster silhouette percentage: 31.79%
- Best tested K: 2
- Best tested silhouette: 0.3477
- 85% target achieved: False

## Segment Profiles
 Segment  Customer_Count  Avg_Recency_Days  Avg_Frequency  Avg_Monetary_INR  Median_Monetary_INR  Churn_Rate_Pct
       0              36         26.611111       4.805556      38911.825000            37423.825        8.333333
       1              75        185.266667       5.000000      43837.178667            42167.900        1.333333
       2              39        206.307692       3.974359      38005.255128            37049.650        5.128205
       3              13        158.307692       2.846154      19978.384615            16376.400        0.000000
       4              37        119.567568       4.405405      20808.814865            20931.800        0.000000

## Limitations
- Only 200 customer profiles were supplied.
- Sales data is not confirmed insurance-policy data.
- Fintech records have no verified customer mapping.
- The five-cluster solution requires business validation.
- Silhouette score is a clustering metric, not prediction accuracy.
- No validated future CLV target is available.

## Interpretation
These results describe the supplied sample dataset only.
They must not be presented as validated insurance CLV findings.