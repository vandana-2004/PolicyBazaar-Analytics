# Week 1 — Data Quality Assessment
## PolicyBazaar Analytics

**Status:** Initial assessment  
**Scope:** Three supplied CSV datasets  
**Raw data policy:** Original files are preserved; no records have been modified.

## 1. Dataset-level checks

| Dataset | Rows | Columns | Missing values | Duplicate rows |
|---|---:|---:|---:|---:|
| Customer Profiles | 200 | 10 | 0 | 0 |
| Sales Transactions | 1,000 | 11 | 0 | 0 |
| Fintech Transactions | 800 | 11 | 0 | 0 |
| **Total** | **2,000** | **32** | **0** | **0** |

## 2. Checks that passed

- Customer profile IDs are unique (200 distinct IDs).
- Sales transaction IDs are unique (1,000 distinct IDs).
- Fintech transaction IDs are unique (800 distinct IDs).
- All 200 customer IDs in the profiles dataset appear in the sales dataset.
- All 200 customer profiles are represented in the sales dataset.
- Date fields inspected so far parse successfully.
- Sales units and unit prices are positive in the inspected records.
- Fintech transaction amounts are non-negative in the inspected records.

## 3. Critical finding: Customer date-order inconsistency

**Severity: High — requires investigation before RFM/CLV calculations.**

42 of 200 customer profiles (21%) have a `First_Purchase_Date` later than their `Last_Purchase_Date`.

Examples include:
- C8: first purchase 2025-09-16; last purchase 2025-07-24.
- C16: first purchase 2026-04-30; last purchase 2025-09-23.
- C108: first purchase 2026-05-30; last purchase 2025-07-11.

This inconsistency may affect customer-history interpretation and recency calculations.

**Recommended action:**
1. Preserve the supplied values in the raw dataset.
2. Flag affected customer records during data preparation.
3. Confirm the correct date definitions or values with the data owner.
4. Do not swap or overwrite dates without verified evidence.
5. Recalculate RFM metrics only after the issue has been investigated or an explicit treatment has been documented.

## 4. Fintech customer-ID linkage limitation

The fintech dataset contains 746 distinct `user_id` values. Its IDs do not exactly match the `Customer_ID` values in the customer profiles dataset.

No verified mapping between these identifiers has been supplied.

**Recommended action:** Keep fintech analysis separate until a valid customer-ID mapping or data dictionary is provided. Do not join these datasets using assumed ID relationships.

## 5. Transaction interpretation checks

The fintech dataset contains:
- Successful transactions: 477
- Pending transactions: 162
- Failed transactions: 161
- Fraud-flagged records: 25

Transaction status and fraud flags must be considered before defining eligible financial activity. Do not treat every recorded transaction as a completed successful transaction.

The sales dataset contains 97 records with `Return_Flag = 1`. Returns should be considered explicitly when defining revenue and customer-value measures.

## 6. Business impact and risks

| Finding | Potential impact | Priority |
|---|---|---|
| 42 customer date inconsistencies | Incorrect customer recency and history | High |
| No verified fintech ID mapping | Incorrect cross-dataset joins | High |
| Pending and failed fintech transactions | Inflated activity if counted as completed | Medium |
| Fraud-flagged fintech records | Distorted financial analysis if not reviewed | Medium |
| Sales return records | Revenue overstatement if returns are ignored | Medium |

## 7. Additional validation checks

The following domain and numeric validation checks returned zero invalid records:

| Dataset | Validation | Invalid records |
|---|---|---:|
| Customer Profiles | Churned values restricted to 0/1 | 0 |
| Customer Profiles | Non-negative Total_Orders | 0 |
| Customer Profiles | Non-negative Total_Revenue | 0 |
| Sales Transactions | Return_Flag restricted to 0/1 | 0 |
| Sales Transactions | Positive Units | 0 |
| Sales Transactions | Positive Unit_Price | 0 |
| Sales Transactions | Discount_Pct between 0 and 100 | 0 |
| Fintech Transactions | is_weekend restricted to 0/1 | 0 |
| Fintech Transactions | is_fraud restricted to 0/1 | 0 |
| Fintech Transactions | Non-negative amount_inr | 0 |
| Fintech Transactions | Status restricted to Success, Pending, Failed | 0 |

These checks passed for all inspected records. They do not resolve the customer date-order inconsistency or the missing fintech customer-ID mapping.
## 8. Overall assessment

The supplied datasets have no missing values or duplicate rows in the initial checks. However, the customer date-order inconsistencies and the absence of a verified fintech-to-customer ID mapping are important limitations.

The data is suitable for continued profiling and documented exploratory analysis, but these issues must be addressed before relying on RFM recency, cross-dataset customer analysis, or final CLV results.

**Assessment status: Initial review completed — remediation and further validation required.**

