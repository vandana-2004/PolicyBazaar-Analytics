from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "week6"

with open(OUT / "cluster_evaluation.json", encoding="utf-8") as f:
    evaluation = json.load(f)

segments = pd.read_csv(OUT / "segment_profiles.csv")
cohorts = pd.read_csv(OUT / "cohort_summary.csv")
retention = pd.read_csv(OUT / "cohort_retention_pct.csv")

total_customers = evaluation["total_customers"]
eligible = evaluation["eligible_customers"]
five = evaluation["five_cluster_silhouette"]
best = evaluation["best_tested_model"]

segment_names = {
    0: "Recently Active, Higher Spending",
    1: "High Spending, At-Risk of Inactivity",
    2: "High Spending, Lapsed",
    3: "Lower Spending, Lower Frequency",
    4: "Moderate Spending, Recently Active",
}

actions = {
    0: "Test relevant cross-sell and repeat-purchase engagement; validate the recorded churn indicator.",
    1: "Prioritize personalized re-engagement and investigate the long gap since the last recorded purchase.",
    2: "Test win-back communication and investigate reasons for inactivity.",
    3: "Explore low-cost education and suitable entry-level offerings; validate customer needs first.",
    4: "Test relevant product education and cross-sell opportunities.",
}

total_observed_revenue = cohorts[
    "Observed_Non_Returned_Revenue_INR"
].sum()

total_cohort_customers = cohorts["Cohort_Size"].sum()

best_cohort = cohorts.loc[
    cohorts["Observed_Revenue_Per_Cohort_Customer_INR"].idxmax()
]

oldest_cohort = cohorts.loc[
    cohorts["Observed_Revenue_Per_Cohort_Customer_INR"].idxmin()
]

retention_month1 = retention["Month_1"].dropna()
month1_average = retention_month1.mean()

lines = [
    "# Week 6 — RFM, Cohort and Customer Value Analysis",
    "",
    "## 1. Executive Summary",
    "",
    f"- Customer sample: **{total_customers}** profiles.",
    f"- RFM eligible customers: **{eligible}**.",
    "- Valid non-returned sales transactions: **903**.",
    f"- Five-cluster silhouette: **{five['silhouette_score']:.4f}** "
    f"({five['silhouette_pct']:.2f}%).",
    f"- Best tested clustering result: **k={best['k']}**, "
    f"silhouette **{best['silhouette_score']:.4f}** "
    f"({best['silhouette_pct']:.2f}%).",
    f"- Observed non-returned discounted sales: **₹{total_observed_revenue:,.2f}**.",
    "",
    "The analysis provides a sample-level view of customer purchasing patterns. "
    "It does not establish insurance policyholder lifetime value.",
    "",
    "## 2. RFM Methodology",
    "",
    "- Recency: days since the latest non-returned transaction.",
    "- Frequency: distinct non-returned sales transactions.",
    "- Monetary: discounted value of non-returned transactions.",
    "- Observation date: 29 June 2026.",
    "- RFM features were log-transformed and standardized before K-Means.",
    "",
    "## 3. Customer Segments and Suggested Experiments",
    "",
    "| Segment | Customers | Avg Recency (days) | Avg Frequency | Avg Monetary (₹) | Churn Rate |",
    "|---:|---:|---:|---:|---:|---:|",
]

for _, row in segments.sort_values("Segment").iterrows():
    segment = int(row["Segment"])
    lines.append(
        f"| {segment} | {int(row['Customer_Count'])} "
        f"| {row['Avg_Recency_Days']:.1f} "
        f"| {row['Avg_Frequency']:.2f} "
        f"| {row['Avg_Monetary_INR']:,.2f} "
        f"| {row['Churn_Rate_Pct']:.2f}% |"
    )

lines += [
    "",
    "### Provisional segment interpretation",
    "",
]

for _, row in segments.sort_values("Segment").iterrows():
    segment = int(row["Segment"])
    lines.append(
        f"- **Segment {segment} — {segment_names[segment]}:** "
        f"{actions[segment]}"
    )

lines += [
    "",
    "These are hypotheses for business testing, not proven customer preferences "
    "or causal effects. Segment churn rates use the supplied profile-level "
    "Churned field.",
    "",
    "## 4. Clustering Evaluation",
    "",
    f"- Requested business segmentation: 5 clusters; silhouette "
    f"{five['silhouette_pct']:.2f}%.",
    f"- Best tested alternative: {best['k']} clusters; silhouette "
    f"{best['silhouette_pct']:.2f}%.",
    "- The 85% acceptance target was not met.",
    "- The five-cluster output is retained to support the requested five-group "
    "business analysis, but cluster separation is modest.",
    "- Silhouette measures cluster separation and cohesion; it is not model "
    "prediction accuracy.",
    "",
    "## 5. Cohort Retention",
    "",
    f"- First-observed-purchase cohorts: {len(cohorts)}.",
    f"- Total cohort customers: {total_cohort_customers}.",
    f"- Mean Month 1 retention across cohorts with an observed Month 1: "
    f"{month1_average:.2f}%.",
    "- Zero-activity months within an observed cohort window are represented "
    "as 0%; months beyond the observation window remain blank.",
    "- Retention is based on at least one non-returned transaction in a month.",
    "",
    "Cohorts have unequal observation windows. Newer cohorts must not be "
    "compared with older cohorts as if they had equal follow-up time.",
    "",
    "## 6. Historical Observed Customer Value",
    "",
    f"- Highest observed revenue per original cohort customer: "
    f"{best_cohort['Cohort_Month']} — "
    f"₹{best_cohort['Observed_Revenue_Per_Cohort_Customer_INR']:,.2f} "
    f"across {int(best_cohort['Cohort_Size'])} customers.",
    f"- Lowest observed revenue per original cohort customer: "
    f"{oldest_cohort['Cohort_Month']} — "
    f"₹{oldest_cohort['Observed_Revenue_Per_Cohort_Customer_INR']:,.2f} "
    f"across {int(oldest_cohort['Cohort_Size'])} customers.",
    f"- Total observed non-returned discounted sales: "
    f"₹{total_observed_revenue:,.2f}.",
    "",
    "These are historical transaction values, not forecasts or customer "
    "lifetime value estimates. Cohort size and observation duration differ.",
    "",
    "## 7. Business Recommendations",
    "",
    "1. Validate the five segment profiles with business stakeholders before "
    "using them for customer campaigns.",
    "2. Test re-engagement experiments on customers with high recency values.",
    "3. Test relevant cross-sell and repeat-purchase experiments for recently "
    "active customers.",
    "4. Measure campaign response, conversion, incremental contribution and "
    "retention using a control group.",
    "5. Obtain verified insurance policy, premium, commission, renewal, "
    "cancellation and acquisition-cost data before building an insurance CLV model.",
    "",
    "## 8. Data Limitations and Acceptance Gaps",
    "",
    "- Only 200 customer profiles were supplied, not the 50,000 target.",
    "- Sales records are not confirmed insurance policy transactions.",
    "- Profile-level Total_Orders and Total_Revenue do not reconcile with "
    "transaction-level sales; RFM therefore uses transaction-derived metrics.",
    "- 42 customer profiles have first-purchase dates later than last-purchase "
    "dates; original dates were not silently altered.",
    "- Fintech user IDs have no verified mapping to customer profile IDs and "
    "were excluded from customer-level RFM and cohort calculations.",
    "- No verified future CLV target or insurance commission outcome is available.",
    "- Five-cluster silhouette is below the stated 85% target.",
    "",
    "## 9. Deliverables",
    "",
    "- `rfm_customer_metrics.csv`",
    "- `customer_segments.csv`",
    "- `segment_profiles.csv`",
    "- `cluster_evaluation.json`",
    "- `rfm_analysis_report.md`",
    "- `cohort_retention_pct.csv`",
    "- `cohort_monthly_revenue_inr.csv`",
    "- `cohort_summary.csv`",
    "- `cohort_analysis_report.md`",
    "- `silhouette_evaluation.png`",
    "- `segment_distribution.png`",
    "- `rfm_distributions.png`",
    "- `cohort_retention_heatmap.png`",
    "- `cohort_revenue_per_customer.png`",
    "",
    "## Conclusion",
    "",
    "Week 6 establishes reproducible sample-level RFM and cohort analyses. "
    "The results can guide further investigation and experiment design, "
    "but cannot yet validate insurance CLV, the 50,000-customer segmentation "
    "target, or the 85% clustering acceptance criterion.",
]

(OUT / "week6_executive_analysis.md").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8-sig",
)

print("WEEK 6 EXECUTIVE REPORT CREATED")
print("Customers:", total_customers)
print("Segments:", len(segments))
print("Cohorts:", len(cohorts))
print("Month 1 average retention:", round(month1_average, 2), "%")
print("Observed non-returned sales: ₹{:,.2f}".format(total_observed_revenue))
print("Report:", OUT / "week6_executive_analysis.md")
