from pathlib import Path
import json

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "reports" / "week6"
OUT.mkdir(parents=True, exist_ok=True)

sales = pd.read_csv(DATA / "da_sales_transactions.csv")

sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
for col in ["Units", "Unit_Price", "Discount_Pct", "Return_Flag"]:
    sales[col] = pd.to_numeric(sales[col], errors="coerce")

sales = sales.dropna(
    subset=["Transaction_ID", "Customer_ID", "Date",
            "Units", "Unit_Price", "Discount_Pct", "Return_Flag"]
).copy()

sales["Discounted_Amount"] = (
    sales["Units"] * sales["Unit_Price"]
    * (1 - sales["Discount_Pct"] / 100)
)

valid = sales[
    (sales["Return_Flag"] == 0)
    & (sales["Discounted_Amount"] >= 0)
].copy()

if valid.empty:
    raise ValueError("No valid non-returned transactions found.")

valid["Activity_Month"] = valid["Date"].dt.to_period("M")
first_purchase = (
    valid.groupby("Customer_ID")["Activity_Month"]
    .min()
    .rename("Cohort_Month")
)
valid = valid.join(first_purchase, on="Customer_ID")

valid["Cohort_Index"] = (
    (valid["Activity_Month"].dt.year - valid["Cohort_Month"].dt.year) * 12
    + valid["Activity_Month"].dt.month
    - valid["Cohort_Month"].dt.month
)

cohort_sizes = (
    first_purchase.value_counts()
    .sort_index()
    .rename("Cohort_Size")
)

active = (
    valid.groupby(["Cohort_Month", "Cohort_Index"])["Customer_ID"]
    .nunique()
    .reset_index(name="Active_Customers")
)

retention = active.pivot(
    index="Cohort_Month",
    columns="Cohort_Index",
    values="Active_Customers"
).sort_index()

last_observed_month = valid["Activity_Month"].max()
max_cohort_index = int(valid["Cohort_Index"].max())
retention = retention.reindex(columns=range(max_cohort_index + 1))

for cohort_month in retention.index:
    max_age = (
        (last_observed_month.year - cohort_month.year) * 12
        + last_observed_month.month - cohort_month.month
    )
    observed_columns = range(max_age + 1)
    retention.loc[cohort_month, observed_columns] = (
        retention.loc[cohort_month, observed_columns].fillna(0)
    )

retention_pct = retention.div(cohort_sizes, axis=0) * 100
retention_pct.index = retention_pct.index.astype(str)
retention_pct.columns = [f"Month_{int(c)}" for c in retention_pct.columns]

retention_pct.to_csv(OUT / "cohort_retention_pct.csv")

revenue = (
    valid.groupby(["Cohort_Month", "Cohort_Index"])["Discounted_Amount"]
    .sum()
    .reset_index()
)

revenue_pivot = revenue.pivot(
    index="Cohort_Month",
    columns="Cohort_Index",
    values="Discounted_Amount"
).sort_index()

revenue_pivot.index = revenue_pivot.index.astype(str)
revenue_pivot.columns = [f"Month_{int(c)}" for c in revenue_pivot.columns]
revenue_pivot.to_csv(OUT / "cohort_monthly_revenue_inr.csv")

total_revenue = valid.groupby("Cohort_Month")["Discounted_Amount"].sum()
observed_months = (
    valid.groupby("Cohort_Month")["Activity_Month"].nunique()
)

summary = pd.DataFrame({
    "Cohort_Size": cohort_sizes,
    "Observed_Non_Returned_Revenue_INR": total_revenue,
    "Observed_Revenue_Per_Cohort_Customer_INR":
        total_revenue / cohort_sizes,
    "Observed_Active_Months": observed_months,
}).sort_index()

summary.index = summary.index.astype(str)
summary.to_csv(OUT / "cohort_summary.csv")

# Retention heatmap
matrix = retention_pct.to_numpy(dtype=float)
fig, ax = plt.subplots(figsize=(12, 6))
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=100, cmap="YlGnBu")
ax.set_title("Customer Cohort Retention (%)")
ax.set_xlabel("Months Since First Observed Purchase")
ax.set_ylabel("First Purchase Cohort")
ax.set_xticks(range(len(retention_pct.columns)))
ax.set_xticklabels(retention_pct.columns, rotation=45)
ax.set_yticks(range(len(retention_pct.index)))
ax.set_yticklabels(retention_pct.index)
fig.colorbar(im, ax=ax, label="Retention (%)")
fig.tight_layout()
fig.savefig(OUT / "cohort_retention_heatmap.png", dpi=150)
plt.close(fig)

# Observed revenue per original cohort customer
fig, ax = plt.subplots(figsize=(11, 5))
summary["Observed_Revenue_Per_Cohort_Customer_INR"].plot(
    kind="bar", ax=ax
)
ax.set_title("Observed Revenue per Cohort Customer")
ax.set_xlabel("First Purchase Cohort")
ax.set_ylabel("INR")
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()
fig.savefig(OUT / "cohort_revenue_per_customer.png", dpi=150)
plt.close(fig)

report = f"""# Week 6 — Customer Cohort and Exploratory Value Analysis

## Scope
- Source: supplied sales transaction sample
- Valid non-returned transactions: {len(valid)}
- Customers represented: {valid['Customer_ID'].nunique()}
- Observation period: {valid['Date'].min().date()} to {valid['Date'].max().date()}
- Cohort assignment: month of first observed non-returned transaction

## Method
- Monthly retention counts distinct customers with a non-returned transaction.
- Retention percentage uses the original cohort size as denominator.
- Monthly revenue is discounted transaction value from non-returned records.
- Observed revenue per cohort customer is cumulative observed revenue divided by original cohort size.

## Important interpretation
These are historical observations from the supplied general sales sample.
Observed revenue per customer is not predicted lifetime value.
It is not confirmed insurance premium, commission, or policyholder CLV.
Cohorts have different observation windows; newer cohorts have had less time to generate activity.
No future revenue has been forecast or extrapolated.

## Outputs
- cohort_retention_pct.csv
- cohort_monthly_revenue_inr.csv
- cohort_summary.csv
- cohort_retention_heatmap.png
- cohort_revenue_per_customer.png
"""
(OUT / "cohort_analysis_report.md").write_text(
    report, encoding="utf-8-sig"
)

print("WEEK 6 COHORT ANALYSIS COMPLETED")
print("Customers:", valid["Customer_ID"].nunique())
print("Valid non-returned transactions:", len(valid))
print("\nCOHORT SUMMARY")
print(summary.to_string())
print("\nOUTPUT DIRECTORY:", OUT)
