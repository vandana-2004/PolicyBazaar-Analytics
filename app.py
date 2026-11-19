
from pathlib import Path
import json

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "dashboard"

st.set_page_config(
    page_title="PolicyBazaar | Final Analytics",
    page_icon="📊",
    layout="wide",
)

SEGMENT_INFO = {
    0: {
        "name": "Recently Active, Higher Spending",
        "priority": "Tier 2 — Retention",
        "action": "Test relevant cross-sell and repeat-purchase engagement. "
                  "Validate the recorded churn indicator.",
    },
    1: {
        "name": "High Spending, At-Risk of Inactivity",
        "priority": "Tier 1 — Re-engagement",
        "action": "Prioritize personalized re-engagement and investigate "
                  "the long gap since the last recorded purchase.",
    },
    2: {
        "name": "High Spending, Lapsed",
        "priority": "Tier 1 — Re-engagement",
        "action": "Test win-back communication and investigate "
                  "reasons for inactivity.",
    },
    3: {
        "name": "Lower Spending, Lower Frequency",
        "priority": "Tier 3 — Education",
        "action": "Explore low-cost education and suitable entry-level "
                  "offerings. Validate customer needs first.",
    },
    4: {
        "name": "Moderate Spending, Recently Active",
        "priority": "Tier 2 — Retention",
        "action": "Test relevant product education and cross-sell "
                  "opportunities.",
    },
}


@st.cache_data
def load_data():
    with open(DATA / "dashboard_kpis.json", encoding="utf-8") as f:
        kpis = json.load(f)

    segments = pd.read_csv(DATA / "segment_summary.csv")
    monthly = pd.read_csv(DATA / "monthly_sales.csv")
    categories = pd.read_csv(DATA / "category_sales.csv")
    retention = pd.read_csv(DATA / "cohort_retention_pct.csv")

    return kpis, segments, monthly, categories, retention


st.title("PolicyBazaar Customer Analytics")
st.caption("Week 12 | Final Dashboard — Customer Segmentation and Growth")

st.warning(
    "IMPORTANT DATA LIMITATION: This dashboard analyses 200 customer "
    "profiles and 1,000 supplied retail sales transactions. Transaction "
    "values, product categories and RFM segments are exploratory proxies. "
    "They are not actual insurance premiums, commissions, claims, renewals "
    "or predicted insurance customer lifetime value. The 50,000+ figure "
    "is a production-scale objective, not the size of this dataset."
)

try:
    kpis, segments, monthly, categories, retention = load_data()
except Exception as exc:
    st.error(f"Dashboard data could not be loaded: {exc}")
    st.stop()


# ---------------------------------------------------------
# Overall performance
# ---------------------------------------------------------

st.header("1. Overall Performance")

a, b, c, d = st.columns(4)
a.metric("Customers", f"{kpis['total_customers']:,}")
b.metric("Sales transactions", f"{kpis['sales_transactions']:,}")
c.metric("Valid transactions", f"{kpis['valid_transactions']:,}")
d.metric("Observed sales", f"₹{kpis['observed_sales_inr']:,.2f}")

a, b, c, d = st.columns(4)
a.metric(
    "Avg. observed sales/customer",
    f"₹{kpis['average_observed_sales_per_customer_inr']:,.2f}",
)
b.metric("Churned customers", f"{kpis['churned_customers']:,}")
c.metric("Average frequency", f"{kpis['average_frequency']:.2f}")
d.metric("Average recency", f"{kpis['average_recency_days']:.1f} days")

st.caption(
    "Observed sales exclude returned transactions and apply recorded "
    "discounts. These are historical retail transaction measures, "
    "not insurance CLV."
)


# ---------------------------------------------------------
# Segment analysis
# ---------------------------------------------------------

st.divider()
st.header("2. Customer Segment Analysis")

segments["Segment"] = segments["Segment"].astype(int)
segments["Segment_Name"] = segments["Segment"].map(
    lambda x: SEGMENT_INFO.get(x, {}).get("name", f"Segment {x}")
)
segments["Priority"] = segments["Segment"].map(
    lambda x: SEGMENT_INFO.get(x, {}).get("priority", "Review")
)
segments["Recommended_Action"] = segments["Segment"].map(
    lambda x: SEGMENT_INFO.get(x, {}).get("action", "Review segment")
)

all_segments = sorted(segments["Segment"].unique().tolist())

selected = st.multiselect(
    "Filter customer segments",
    options=all_segments,
    default=all_segments,
    format_func=lambda x: (
        f"Segment {x} — "
        f"{SEGMENT_INFO.get(x, {}).get('name', 'Other')}"
    ),
)

view = segments[segments["Segment"].isin(selected)].copy()

if view.empty:
    st.info("Select at least one segment to display the analysis.")
else:
    left, right = st.columns(2)

    left.write("**Customer count by segment**")
    left.bar_chart(
        view.set_index("Segment_Name")[["Customer_Count"]]
    )

    right.write("**Observed sales by segment**")
    right.bar_chart(
        view.set_index("Segment_Name")[["Observed_Sales_INR"]]
    )

    st.subheader("Segment KPI and Action Table")

    display_columns = [
        "Segment",
        "Segment_Name",
        "Priority",
        "Customer_Count",
        "Avg_Recency_Days",
        "Avg_Frequency",
        "Avg_Monetary_INR",
        "Churn_Rate_Pct",
        "Recommended_Action",
    ]

    st.dataframe(
        view[display_columns].round(2),
        width="stretch",
        hide_index=True,
    )

    left, right = st.columns(2)
    left.metric(
        "Customers in selected segments",
        f"{int(view['Customer_Count'].sum()):,}",
    )
    right.metric(
        "Observed sales in selected segments",
        f"₹{view['Observed_Sales_INR'].sum():,.2f}",
    )


# ---------------------------------------------------------
# Business action priorities
# ---------------------------------------------------------

st.divider()
st.header("3. Three-Tier Business Action Strategy")

st.caption(
    "These are proposed experiments based on observed retail purchasing "
    "patterns. They are not validated insurance customer preferences."
)

tiers = [
    (
        "Tier 1 — Re-engagement",
        [1, 2],
        "Prioritize Segments 1 and 2. Test personalized re-engagement "
        "and win-back communication. Investigate inactivity before "
        "selecting an offer.",
    ),
    (
        "Tier 2 — Retention and Engagement",
        [0, 4],
        "Focus on Segments 0 and 4. Test relevant product education, "
        "cross-sell and repeat-purchase engagement. Segment 0 has the "
        "highest recorded profile-level churn rate in this sample.",
    ),
    (
        "Tier 3 — Low-Cost Education",
        [3],
        "Explore low-cost educational communication and suitable "
        "entry-level offerings. Validate customer needs before "
        "making product recommendations.",
    ),
]

for title, ids, description in tiers:
    tier_data = segments[segments["Segment"].isin(ids)]
    count = int(tier_data["Customer_Count"].sum())

    with st.expander(f"{title} — {count} customers", expanded=True):
        st.write(description)
        st.write(
            "Included segments: "
            + ", ".join(str(x) for x in ids)
        )
        st.metric("Customers in this tier", f"{count:,}")


# ---------------------------------------------------------
# Illustrative impact scenario
# ---------------------------------------------------------

st.divider()
st.header("4. Illustrative Business Impact Scenario")

st.warning(
    "HYPOTHETICAL SCENARIO ONLY — This calculation applies assumed "
    "response and uplift percentages to historical retail monetary "
    "values. It is not actual insurance revenue, commission, profit, "
    "predictive CLV or a guaranteed campaign outcome."
)

scenario_assumptions = {
    1: {"response": 0.10, "uplift": 0.05},
    2: {"response": 0.08, "uplift": 0.05},
    3: {"response": 0.05, "uplift": 0.03},
}

scenario_rows = []

for tier_name, ids, _ in tiers:
    tier_data = segments[segments["Segment"].isin(ids)]

    if len(tier_data) != len(ids):
        continue

    customer_count = int(tier_data["Customer_Count"].sum())
    historical_value = float(
        (tier_data["Customer_Count"] *
         tier_data["Avg_Monetary_INR"]).sum()
    )

    assumption = scenario_assumptions[len(scenario_rows) + 1]
    estimated_impact = (
        historical_value
        * assumption["response"]
        * assumption["uplift"]
    )

    scenario_rows.append({
        "Action Tier": tier_name,
        "Customers": customer_count,
        "Assumed Response": f"{assumption['response']:.0%}",
        "Assumed Incremental Uplift": f"{assumption['uplift']:.0%}",
        "Illustrative Impact INR": estimated_impact,
    })

scenario = pd.DataFrame(scenario_rows)
total_impact = scenario["Illustrative Impact INR"].sum()

st.dataframe(
    scenario.style.format(
        {"Illustrative Impact INR": "₹{:,.2f}"}
    ),
    width="stretch",
    hide_index=True,
)

st.metric(
    "Total illustrative impact",
    f"₹{total_impact:,.2f}",
)

st.caption(
    "Formula: segment historical monetary value × assumed response "
    "rate × assumed incremental uplift. Assumptions have not been "
    "validated through campaigns or a control group."
)


# ---------------------------------------------------------
# Acceptance criteria tracker
# ---------------------------------------------------------

st.divider()
st.header("5. Project Acceptance Criteria")

acceptance = pd.DataFrame([
    {
        "Requirement": "Five customer segments",
        "Evidence": "Five clusters represented in the supplied 200-customer sample.",
        "Status": "Achieved for sample",
    },
    {
        "Requirement": "Silhouette score >= 0.85",
        "Evidence": "Five-cluster silhouette = 0.3179.",
        "Status": "Not achieved",
    },
    {
        "Requirement": "CLV model MAE < ₹500",
        "Evidence": "No validated future insurance CLV target or prediction horizon.",
        "Status": "Not demonstrated",
    },
    {
        "Requirement": "Segment-filterable dashboard",
        "Evidence": "Streamlit segment multiselect and filtered charts/table.",
        "Status": "Implemented",
    },
    {
        "Requirement": "Three-tier upsell strategy",
        "Evidence": "Three proposed action tiers with segment assignments.",
        "Status": "Proposed",
    },
    {
        "Requirement": "Quantified INR impact",
        "Evidence": "Illustrative scenario using explicit assumptions.",
        "Status": "Illustrative only",
    },
    {
        "Requirement": "50,000+ policyholder scale",
        "Evidence": "Current sample contains 200 profiles; production-scale benchmark unavailable.",
        "Status": "Not validated",
    },
])

st.dataframe(
    acceptance,
    width="stretch",
    hide_index=True,
)

st.caption(
    "Statuses distinguish implemented deliverables from unmet or "
    "unvalidated business acceptance targets."
)


# ---------------------------------------------------------
# Monthly sales
# ---------------------------------------------------------

st.divider()
st.header("6. Monthly Observed Sales")

monthly["Month"] = monthly["Month"].astype(str)
monthly = monthly.sort_values("Month")

st.line_chart(
    monthly.set_index("Month")[["Observed_Sales_INR"]]
)
st.dataframe(monthly, width="stretch", hide_index=True)


# ---------------------------------------------------------
# Product categories
# ---------------------------------------------------------

st.divider()
st.header("7. Product Category Analysis")

categories = categories.sort_values(
    "Observed_Sales_INR",
    ascending=False,
)

st.bar_chart(
    categories.set_index("Category")[["Observed_Sales_INR"]]
)
st.dataframe(categories, width="stretch", hide_index=True)

st.caption(
    "Categories are from the supplied retail transaction data, "
    "not verified insurance product categories."
)


# ---------------------------------------------------------
# Cohort retention
# ---------------------------------------------------------

st.divider()
st.header("8. Cohort Retention")

st.caption(
    "Percentages represent observed cohort retention. Blank cells "
    "indicate periods not observed in the dataset. Cohorts have "
    "unequal observation windows."
)

retention = retention.set_index("Cohort_Month")

st.dataframe(
    retention.style.format("{:.1f}%", na_rep="—"),
    width="stretch",
)


# ---------------------------------------------------------
# Methodology and limitations
# ---------------------------------------------------------

st.divider()

with st.expander("Methodology, assumptions and limitations"):
    st.markdown(
        """
        **Data sources**
        - Week 6 customer segmentation output.
        - Supplied retail sales transactions aggregated into dashboard files.
        - Week 6 cohort retention output.

        **Metric definitions**
        - Recency: days since the latest non-returned transaction at the
          Week 6 observation date.
        - Frequency: distinct non-returned sales transaction frequency.
        - Monetary: historical discounted value of non-returned sales.
        - Observed sales: units × unit price × (1 − discount percentage),
          excluding returned transactions.
        - Churn rate: percentage marked churned in supplied customer profiles.

        **Important data limitations**
        - The supplied sample contains 200 profiles and 1,000 retail sales
          transactions, not 50,000 insurance policyholders.
        - Profile-reported revenue and transaction-derived monetary values
          are different measures and should not be conflated.
        - Retail transaction values and categories are exploratory proxies,
          not actual insurance premiums, commissions, claims or renewals.
        - Fintech records are not joined because verified customer ID
          mapping is unavailable.
        - Historical monetary value is not predictive customer lifetime value.
        - No validated future insurance CLV target or prediction horizon
          is available to calculate model MAE.
        - Five-cluster silhouette is approximately 0.3179, below the
          stated 0.85 target. The best tested two-cluster result was
          approximately 0.3477.
        - Silhouette measures cluster separation and cohesion; it is
          not prediction accuracy.
        - Segment interpretations and proposed actions are hypotheses,
          not proven customer preferences or causal effects.

        **Production-scale considerations**
        - Reuse data validation and feature engineering with verified
          customer and policy identifiers.
        - Benchmark processing and clustering on the actual production
          dataset before claiming 50,000+ scale readiness.
        - Obtain verified premiums, commissions, renewals, cancellations
          and acquisition costs before developing an insurance CLV model.
        - Validate campaigns using response, conversion, incremental
          contribution and retention, ideally with a control group.
        """
    )

st.caption(
    "PolicyBazaar Analytics | Week 12 Final Dashboard | "
    "Exploratory sample analysis — not validated insurance CLV"
)
