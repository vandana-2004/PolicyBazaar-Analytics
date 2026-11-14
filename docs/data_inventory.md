# PolicyBazaar Analytics
## Week 1 — Data Inventory

## 1. Objective

This inventory documents the three datasets supplied for the PolicyBazaar Analytics project. It records dataset structure, volume, fields, data types, identifier characteristics, date coverage and suitability for the planned analysis.

## 2. Dataset Overview

| Dataset | Records | Columns | File |
|---|---:|---:|---|
| Customer Profiles | 200 | 10 | da_customer_profiles.csv |
| Sales Transactions | 1,000 | 11 | da_sales_transactions.csv |
| Fintech Transactions | 800 | 11 | da_fintech_transactions.csv |
| Total | 2,000 | 32 | 3 CSV files |

## 3. Customer Profiles

**Purpose:** Contains customer-level demographic, acquisition, purchase and churn information.

**Grain:** One record per customer.

**Primary identifier:** Customer_ID.

| Column | Data type | Description |
|---|---|---|
| Customer_ID | String | Unique customer identifier |
| City | String | Customer city |
| Age_Band | String | Customer age group |
| Gender | String | Gender category |
| Acquisition_Channel | String | Customer acquisition source |
| First_Purchase_Date | Date candidate | First purchase date |
| Total_Orders | Integer | Total number of orders |
| Total_Revenue | Integer | Recorded total revenue |
| Last_Purchase_Date | Date candidate | Most recent purchase date |
| Churned | Integer | Churn indicator |

**Verified characteristics:**
- 200 records.
- 10 columns.
- 200 unique Customer_ID values.
- No missing values.
- No completely duplicated rows.
- First purchase date range: 14 July 2024 to 30 May 2026.
- Last purchase date range: 8 July 2025 to 7 July 2026.
- 42 of 200 customer profiles (21%) have a first purchase date later than their last purchase date. This requires investigation before RFM recency calculations.

**Data quality action:** Preserve the original dates, flag affected records, and request clarification from the data owner. Do not swap or overwrite dates without verified evidence.

## 4. Sales Transactions

**Purpose:** Contains individual sales transaction information, including products, quantities, prices, discounts and returns.

**Grain:** One record per transaction.

**Primary identifier:** Transaction_ID.

| Column | Data type | Description |
|---|---|---|
| Transaction_ID | String | Unique transaction identifier |
| Date | Date candidate | Transaction date |
| Customer_ID | String | Customer reference |
| Product_ID | String | Product reference |
| Category | String | Product category |
| Units | Integer | Units purchased |
| Unit_Price | Integer | Price per unit |
| Discount_Pct | Integer | Discount percentage |
| Channel | String | Sales channel |
| City | String | Transaction city |
| Return_Flag | Integer | Return indicator |

**Verified characteristics:**
- 1,000 records.
- 11 columns.
- 1,000 unique Transaction_ID values.
- All 200 customer profile IDs are represented.
- No unmatched Sales Transactions Customer_ID values.
- No missing values.
- No completely duplicated rows.
- Transaction date range: 2 July 2024 to 28 June 2026.

## 5. Fintech Transactions

**Purpose:** Contains financial transaction information, including transaction types, categories, amounts, merchants and status.

**Grain:** One record per transaction.

**Primary identifier:** txn_id.

| Column | Data type | Description |
|---|---|---|
| txn_id | String | Unique transaction identifier |
| user_id | String | Financial transaction user reference |
| date | Date candidate | Transaction date |
| txn_type | String | Transaction type |
| category | String | Transaction category |
| amount_inr | Decimal | Transaction amount in INR |
| merchant | String | Merchant name |
| city | String | Transaction city |
| status | String | Transaction status |
| is_weekend | Integer | Weekend indicator |
| is_fraud | Integer | Fraud indicator |

**Verified characteristics:**
- 800 records.
- 11 columns.
- 800 unique txn_id values.
- 746 distinct user_id values.
- Repeated user IDs occur across transactions.
- No missing values.
- No completely duplicated rows.
- Transaction date range: 2 January 2023 to 30 December 2024.

## 6. Data Type Assessment

The initial CSV inspection identified:
- Text fields represented as strings.
- Numeric counts and indicators represented as integers.
- Financial amounts represented as integers or decimals.
- Date fields initially imported as strings.

**Required preparation:**

Date columns must be converted into proper datetime values during the data pipeline stage. Indicator fields and monetary values must also be checked for valid ranges and consistent interpretation.

## 7. Identifier and Relationship Assessment

### Customer Profiles and Sales Transactions

The Customer_ID field exists in both datasets.

Verified relationship:
- All 200 customer profile IDs appear in Sales Transactions.
- No unmatched sales customer IDs were identified.

This provides a usable customer-to-sales relationship.

### Customer Profiles and Fintech Transactions

The Customer_ID and user_id fields use different identifier formats.

Verified relationship:
- Customer identifiers use the C-prefixed format.
- Fintech user identifiers use the USR-prefixed format.
- No exact identifier matches were found.

A reliable customer-level relationship cannot currently be established.

**Recommendation:** Request an approved identifier mapping or clarification from the data provider. Do not join these datasets using assumed identifier relationships.

## 8. Business Relevance Assessment

| Dataset | Potential analytical use | Limitation |
|---|---|---|
| Customer Profiles | Customer profiling, churn and customer-level metrics | Only 200 profiles |
| Sales Transactions | Purchase frequency, revenue and product behaviour | General sales rather than explicit insurance policy records |
| Fintech Transactions | Financial transaction patterns | Customer linkage and insurance relevance unconfirmed |

The business relevance of the supplied datasets must be confirmed before combining them for insurance CLV modelling.

## 9. Coverage and Scope Gaps

The project brief specifies 50,000 policyholders.

Current supplied data:
- 200 customer profiles.
- 1,000 sales transactions.
- 800 fintech transactions.

The supplied data therefore does not establish coverage of the required 50,000 policyholders.

The datasets also do not explicitly provide:
- Insurance policy identifiers.
- Policy premium history.
- Renewal history.
- Claims history.
- Confirmed insurance customer mapping.
- A defined CLV prediction target and horizon.

These gaps must be raised with the stakeholder or data provider.

## 10. Recommendations

1. Request confirmation of the complete 50,000-policyholder dataset.
2. Confirm whether the sales dataset represents insurance-related transactions.
3. Request clarification or mapping for fintech user identifiers.
4. Confirm the business definition of customer lifetime value.
5. Confirm the prediction horizon and available historical outcome data.
6. Preserve original datasets and perform transformations on separate working copies.
7. Validate all relationships before customer-level modelling.

## 11. Conclusion

The three supplied datasets contain 2,000 records and 32 columns in total.

Customer Profiles and Sales Transactions have a verified customer identifier relationship. Fintech Transactions cannot currently be linked directly to the customer profiles.

The data provides an initial foundation for exploratory analysis, but additional clarification and potentially additional insurance-specific data are required before the full project acceptance criteria can be evaluated.

---

**Document:** PolicyBazaar Analytics — Week 1 Data Inventory  
**Status:** Reviewed — data inventory and initial data quality assessment completed; final milestone submission pending.

