# PolicyBazaar Analytics
## Week 1 — Stakeholder Brief

**Project:** Customer Lifetime Value Analysis for an Insurance Comparison Portal  
**Client Industry:** InsurTech  
**Client Location:** Gurugram  
**Project Duration:** 3 Months  
**Role:** Data Analyst Intern  
**Milestone:** Week 1 — Stakeholder Brief and Data Inventory

---

## 1. Business Background

PolicyBazaar Analytics is an analytical project for an insurance comparison portal. The business objective is to understand customer value, identify meaningful customer segments, improve customer retention, and develop targeted upselling strategies.

The project brief specifies an expected population of 50,000 policyholders. The analysis will use RFM (Recency, Frequency, Monetary) analysis and K-Means clustering to identify five customer segments.

A Customer Lifetime Value (CLV) prediction model will be developed, and findings will be presented through a segment-filterable Streamlit application.

## 2. Business Problem

The business needs a data-driven understanding of:

- Which customers contribute the most value.
- How customer purchasing behaviour differs.
- Which customers may require retention attention.
- Which customer groups have opportunities for additional insurance products.
- How targeted upselling could contribute to measurable business impact.

The analysis must produce actionable insights rather than only descriptive statistics.

## 3. Simulated Stakeholder Interview

**Method:** Simulated stakeholder discussion based on the supplied project brief.

### Question 1: What is the primary business objective?

**Analytical interpretation:**

Understand customer lifetime value and segment policyholders into five actionable groups to support retention and upselling decisions.

### Question 2: Which customer population should be analysed?

**Requirement from brief:**

50,000 policyholders.

**Clarification required:**

The supplied files currently contain 200 customer profiles, 1,000 sales transactions and 800 fintech transactions. The availability of the remaining policyholder records must be confirmed.

### Question 3: What segmentation approach is expected?

**Requirement from brief:**

RFM analysis combined with K-Means clustering, producing five distinct customer segments with a target silhouette score of at least 85%.

### Question 4: How will customer value be measured?

**Requirement from brief:**

Build a CLV prediction model with a target Mean Absolute Error (MAE) below ₹500.

**Clarification required:**

The business must confirm the definition and prediction horizon of CLV, along with the availability of historical policy and premium information.

### Question 5: How will the analytical findings be used?

**Requirement from brief:**

Develop a segment-filterable Streamlit application and a three-tier upselling strategy document with quantified business impact in Indian rupees.

## 4. Five Analytical Questions

| No. | Analytical question | Business purpose |
|---|---|---|
| 1 | What are the five most meaningful customer segments based on RFM behaviour? | Customer segmentation |
| 2 | Which customer segments generate the highest revenue and purchase frequency? | Revenue contribution |
| 3 | How accurately can customer lifetime value be predicted? | CLV modelling |
| 4 | Which customers or segments show indicators of churn or declining engagement? | Retention planning |
| 5 | Which customer segments offer the strongest opportunities for targeted insurance upselling? | Revenue growth |

These questions will guide the subsequent analytical milestones.

## 5. Project Scope

### In Scope

- Data inventory and data quality assessment.
- Customer-level exploratory data analysis.
- RFM feature engineering.
- K-Means customer segmentation.
- CLV prediction modelling.
- Model evaluation using MAE.
- Segment-level business recommendations.
- Three-tier upselling strategy.
- Streamlit dashboard development.
- Business impact estimation in INR.

### Out of Scope

- Accessing or modifying actual customer insurance accounts.
- Executing insurance sales campaigns.
- Making unsupported financial impact claims.
- Treating simulated or incomplete data as verified production data.

## 6. Acceptance Criteria

| Deliverable | Client target |
|---|---|
| Customer segmentation | 5 distinct segments |
| Clustering quality | Silhouette score ≥ 0.85 |
| CLV prediction | MAE < ₹500 |
| Dashboard | Streamlit app filterable by segment |
| Upselling strategy | 3 tiers |
| Business impact | Quantified in ₹ |

These are target acceptance criteria, not results already achieved.

## 7. Initial Data Observations

The three supplied datasets have been downloaded and locally verified.

| Dataset | Records | Columns |
|---|---:|---:|
| Customer Profiles | 200 | 10 |
| Sales Transactions | 1,000 | 11 |
| Fintech Transactions | 800 | 11 |
| **Total** | **2,000** | **32** |

Initial observations:

- Customer Profiles contains customer-level information, including acquisition channel, purchase dates, total orders, total revenue and churn status.
- Sales Transactions contains transaction-level information, including product, category, units, price, discount, channel and return flag.
- Fintech Transactions contains user-level transaction information, including transaction type, category, amount, merchant and fraud indicator.
- Sales transaction customer identifiers match the customer profile identifier format.
- Fintech user identifiers use a different format and require further investigation before customer-level integration.

## 8. Risks and Clarifications Required

1. The brief specifies 50,000 policyholders, whereas only 200 customer profiles have been supplied.
2. The relationship between fintech user IDs and customer IDs is not established.
3. The relevance of general sales and fintech transactions to insurance policyholder CLV must be confirmed.
4. Policy purchase, renewal, premium and claim information may be needed for a meaningful insurance CLV definition.
5. The business meaning and prediction horizon of CLV must be clarified.
6. The 85% silhouette target needs confirmation of the intended scoring convention and validation method.

## 9. Week 1 Deliverables

- [x] Project workspace created.
- [x] Three original datasets downloaded and verified.
- [x] Stakeholder brief documented.
- [x] Five analytical questions documented.
- [x] Detailed data inventory completed.
- [x] Data quality assessment completed.
- [x] Risks and data limitations documented.
- [ ] Final milestone submission prepared.

## 10. Conclusion

The project has a clear business direction: customer segmentation, lifetime value prediction, retention analysis and targeted upselling.

The initial data inventory establishes three available datasets. However, the difference between the specified 50,000 policyholders and the 200 supplied customer profiles is a significant limitation that must be resolved or formally acknowledged before advanced modelling.

Week 1 will establish a reliable analytical foundation and document the questions that must be answered before proceeding to the data pipeline and baseline metrics.

---

**Document:** PolicyBazaar Analytics — Week 1 Stakeholder Brief  
**Status:** Reviewed — Week 1 documentation and quality assessment completed; final milestone submission pending.

