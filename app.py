from pathlib import Path
import json
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "dashboard"

st.set_page_config(
    page_title="PolicyBazaar | Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("PolicyBazaar Customer Analytics")
st.caption("Week 9 | Aggregate Dashboard v1")

st.warning(
    "Cynaris-confirmed project sample: 200 customer profiles and 1,000 "
    "sales transactions. Transaction values, product categories and "
    "customer segments are exploratory proxies for insurance-relevant "
    "analysis, not actual premiums, commissions or predicted insurance CLV. "
    "The methodology is designed to scale to 50,000+ policyholders."
)

@st.cache_data
def load_data():
    with open(DATA / "dashboard_kpis.json", encoding="utf-8") as f:
        kpis = json.load(f)

    segments = pd.read_csv(DATA / "segment_summary.csv")
    monthly = pd.read_csv(DATA / "monthly_sales.csv")
    categories = pd.read_csv(DATA / "category_sales.csv")
    retention = pd.read_csv(DATA / "cohort_retention_pct.csv")

    return kpis, segments, monthly, categories, retention

try:
    kpis, segments, monthly, categories, retention = load_data()
except Exception as exc:
    st.error(f"Dashboard data could not be loaded: {exc}")
    st.stop()

st.subheader("Overall Performance")

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
    "Overall KPIs describe the complete supplied sample. "
    "Observed sales exclude returned transactions and apply recorded discounts."
)

st.divider()
st.subheader("Segment Analysis")

all_segments = sorted(segments["Segment"].unique().tolist())
selected = st.multiselect(
    "Select customer segments",
    options=all_segments,
    default=all_segments,
)

view = segments[segments["Segment"].isin(selected)].copy()

if view.empty:
    st.info("Select at least one segment to display segment analysis.")
else:
    left, right = st.columns(2)

    left.write("**Customer count by segment**")
    left.bar_chart(view.set_index("Segment")[["Customer_Count"]])

    right.write("**Observed sales by segment**")
    right.bar_chart(view.set_index("Segment")[["Observed_Sales_INR"]])

    st.write("**Segment KPI table**")
    st.dataframe(
        view.round(2),
        width="stretch",
        hide_index=True,
    )

    st.metric(
        "Customers in selected segments",
        f"{int(view['Customer_Count'].sum()):,}",
    )
    st.metric(
        "Observed sales in selected segments",
        f"₹{view['Observed_Sales_INR'].sum():,.2f}",
    )

st.divider()
st.subheader("Monthly Observed Sales")

monthly["Month"] = monthly["Month"].astype(str)
monthly = monthly.sort_values("Month")

st.line_chart(
    monthly.set_index("Month")[["Observed_Sales_INR"]]
)

st.dataframe(monthly, width="stretch", hide_index=True)

st.divider()
st.subheader("Product Category Analysis")

categories = categories.sort_values(
    "Observed_Sales_INR", ascending=False
)

st.bar_chart(
    categories.set_index("Category")[["Observed_Sales_INR"]]
)
st.dataframe(categories, width="stretch", hide_index=True)

st.divider()
st.subheader("Cohort Retention")

st.caption(
    "Percentages represent observed cohort retention. "
    "Blank cells indicate periods not observed in the dataset."
)

retention = retention.set_index("Cohort_Month")
st.dataframe(
    retention.style.format("{:.1f}%", na_rep="—"),
    width="stretch",
)

st.divider()

with st.expander("Methodology and limitations"):
    st.markdown(
        """
        **Data sources**
        - Week 6 customer segmentation output
        - Supplied retail sales transactions, aggregated before deployment
        - Week 6 cohort retention output

        **Metric definitions**
        - Recency: days since last purchase at the Week 6 observation date.
        - Frequency: valid non-returned transaction frequency.
        - Monetary: historical discounted sales.
        - Observed sales: units × unit price × (1 − discount percentage),
          excluding returned transactions.
        - Churn rate: percentage marked churned in supplied profiles.

        **Proxy assumptions and limitations**
        - The 200 customer profiles and 1,000 sales transactions are the
          intended Cynaris project sample.
        - Transaction values, product categories and RFM segments are
          exploratory proxies, not actual insurance premiums, commissions,
          claims, renewals or predicted insurance CLV.
        - Fintech records are not joined because verified customer ID
          mapping is unavailable.
        - Historical monetary value is not predictive CLV.
        - Five-cluster silhouette score is approximately 0.318,
          below the stated 0.85 target.

        **Scalability to 50,000+ policyholders**
        - Reuse the data validation and feature-engineering pipeline.
        - Use stable customer and policy identifiers for reliable joins.
        - Process larger datasets in batches or scheduled pipelines.
        - Re-evaluate clustering and segment stability at production scale.
        - Add verified premiums, commissions, renewals and acquisition costs
          when available.
        - Benchmark performance on the larger dataset before deployment.
        """
    )

st.caption("PolicyBazaar Analytics | Week 9 Dashboard v1")
