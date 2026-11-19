# PolicyBazaar Analytics

## Final Strategic Brief — Customer Segmentation, Retention and Growth



**Project:** Customer Lifetime Value Analysis for an Insurance Comparison Portal

**Reporting scope:** Supplied sample data only

**Final milestone:** Week 12



### 1. Situation



The project aims to help an insurance comparison portal understand customer value, identify actionable customer segments, improve retention and develop targeted upselling strategies.



The original brief specifies 50,000 policyholders, five customer segments, a CLV prediction model with MAE below ₹500, a segment-filterable Streamlit application and a three-tier upselling strategy.



The supplied datasets contain 200 customer profiles, 1,000 general sales transactions and 800 fintech transactions. The customer profile and sales transaction identifiers can be linked, but fintech user IDs have no verified customer mapping.



Consequently, the completed analysis uses the supplied retail sales sample as an exploratory proxy. It does not establish actual insurance premiums, commissions, claims, renewals or predicted insurance CLV.



### 2. Key findings



**Historical sales performance**



\- Customer profiles analysed: 200.

\- Sales transactions: 1,000.

\- Non-returned transactions: 903.

\- Observed non-returned discounted sales: ₹72,00,464.20.

\- Average transaction-derived observed sales per customer: ₹36,002.32.

\- Profile-reported average revenue per customer: ₹24,963.10.

\- Profile-recorded churn: 6 customers, or 3%.



The two average customer-value figures use different source fields and calculation methods. They should not be interpreted as equivalent measures.



**Customer segmentation**



Five K-Means segments were retained for exploratory business analysis.



\- Segment 0: 36 customers, recently active, average recency 27 days and recorded churn rate 8.33%.

\- Segment 1: 75 customers, average recency 185 days and average historical monetary value ₹43,837.

\- Segment 2: 39 customers, average recency 206 days and average historical monetary value ₹38,005.

\- Segment 3: 13 customers, lower average frequency and average historical monetary value ₹19,978.

\- Segment 4: 37 customers, average recency 120 days and average historical monetary value ₹20,809.



The five-cluster silhouette score is 0.3179. The best tested alternative, with two clusters, achieved 0.3477. Neither meets the stated 0.85 target.



These clusters are exploratory and require business validation before operational use.



### 3. Three prioritised recommendations



**Priority 1 — Reactivation of high-value inactive customers**



Target segments 1 and 2, comprising 114 customers.



Test personalised re-engagement communications and relevant product education. Measure response, conversion and repeat activity against a control group.



**Priority 2 — Retention and engagement**



Prioritise segment 0 because it has the highest recorded churn rate. Include segment 4 in relevant engagement and product-education experiments.



Measure retention, repeat activity and incremental contribution rather than relying solely on historical transaction values.



**Priority 3 — Low-cost customer education**



Target segment 3 with educational communications and suitable entry-level product information.



Validate customer needs and campaign response before recommending insurance products. Avoid assuming that historical retail purchasing behaviour establishes insurance suitability.



### 4. Illustrative INR impact scenario



The following is a planning scenario, not a forecast or validated insurance revenue estimate.



| Experiment | Customers | Assumed response | Assumed incremental uplift | Illustrative impact |

|---|---:|---:|---:|---:|

| Reactivation — segments 1 and 2 | 114 | 10% | 5% | ₹23,850 |

| Retention/engagement — segments 0 and 4 | 73 | 8% | 5% | ₹8,683 |

| Education — segment 3 | 13 | 5% | 3% | ₹390 |

| **Total** | **200** | | | **₹32,923** |



**Calculation method:** Segment customer count × segment average historical monetary value × assumed response rate × assumed incremental uplift.



The assumptions are illustrative and have not been validated through campaign experiments. The resulting amount is a hypothetical uplift against historical retail monetary values. It is not insurance revenue, commission, profit, predicted CLV or a guaranteed business outcome.



Before using this scenario for budgeting, the business should validate the response and uplift assumptions using controlled experiments and verified insurance transaction data.



### 5. Implications and next steps



The current analysis establishes a repeatable sample-level RFM and cohort workflow and a segment-filterable Streamlit dashboard.



The following work is necessary before production acceptance:



1\. Obtain the intended 50,000-policyholder dataset or an approved explanation of the sample limitation.

2\. Obtain verified policy, premium, commission, renewal, cancellation and claims information.

3\. Define the CLV prediction target and forecast horizon.

4\. Develop and validate a predictive model against a genuine future-value outcome.

5\. Reassess segmentation quality and stability on representative insurance data.

6\. Validate the three recommended experiments through controlled campaigns.



### 6. Acceptance status



| Requirement | Evidence-based status |

|---|---|

| Five customer segments | Completed for supplied sample |

| Silhouette ≥ 0.85 | Not achieved; five-cluster score 0.3179 |

| CLV MAE below ₹500 | Not demonstrated; no validated CLV target |

| Segment-filterable Streamlit app | Implemented in Week 9 |

| Three-tier upselling strategy | Proposed in this brief |

| Quantified INR impact | Illustrative scenario; requires validation |

| 50,000-policyholder coverage | Not achieved; only 200 profiles supplied |



**Conclusion**



The project provides an exploratory foundation for customer segmentation, retention planning and business experimentation. Its strongest immediate opportunity is to test reactivation and retention strategies among the identified customer groups.



The findings must remain explicitly sample-level and proxy-based until verified insurance data is available. Production CLV prediction, the stated clustering quality target and 50,000-policyholder validation remain outstanding.
