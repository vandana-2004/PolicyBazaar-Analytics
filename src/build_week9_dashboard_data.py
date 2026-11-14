from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WEEK6 = ROOT / "reports" / "week6"
OUT = ROOT / "data" / "dashboard"
OUT.mkdir(parents=True, exist_ok=True)

customers = pd.read_csv(WEEK6 / "customer_segments.csv")
sales = pd.read_csv(RAW / "da_sales_transactions.csv")
retention = pd.read_csv(WEEK6 / "cohort_retention_pct.csv")

sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
for col in ["Units", "Unit_Price", "Discount_Pct", "Return_Flag"]:
    sales[col] = pd.to_numeric(sales[col], errors="coerce").fillna(0)

sales["Gross_Sales_INR"] = sales["Units"] * sales["Unit_Price"]
sales["Discounted_Sales_INR"] = (
    sales["Gross_Sales_INR"] * (1 - sales["Discount_Pct"] / 100)
)
sales["Is_Returned"] = sales["Return_Flag"].eq(1)

# Join only for aggregation; customer IDs are never written to output.
joined = sales.merge(
    customers[["Customer_ID", "Segment"]],
    on="Customer_ID",
    how="inner",
    validate="many_to_one",
)

valid = joined.loc[~joined["Is_Returned"]].copy()
valid["Month"] = valid["Date"].dt.to_period("M").astype(str)

segment_base = customers.groupby("Segment").agg(
    Customer_Count=("Customer_ID", "nunique"),
    Avg_Recency_Days=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary_INR=("Monetary", "mean"),
    Median_Monetary_INR=("Monetary", "median"),
    Churned_Customers=("Churned", "sum"),
).reset_index()

segment_base["Churn_Rate_Pct"] = (
    segment_base["Churned_Customers"]
    / segment_base["Customer_Count"] * 100
)

segment_sales = joined.groupby("Segment").agg(
    Sales_Transactions=("Transaction_ID", "count"),
).reset_index()

segment_valid = valid.groupby("Segment").agg(
    Valid_Transactions=("Transaction_ID", "count"),
    Observed_Sales_INR=("Discounted_Sales_INR", "sum"),
).reset_index()

segment_summary = (
    segment_base
    .merge(segment_sales, on="Segment", how="left")
    .merge(segment_valid, on="Segment", how="left")
)

for col in [
    "Sales_Transactions", "Valid_Transactions", "Observed_Sales_INR"
]:
    segment_summary[col] = segment_summary[col].fillna(0)

segment_summary.to_csv(OUT / "segment_summary.csv", index=False)

monthly = valid.groupby("Month").agg(
    Observed_Sales_INR=("Discounted_Sales_INR", "sum"),
    Transactions=("Transaction_ID", "count"),
).reset_index()
monthly.to_csv(OUT / "monthly_sales.csv", index=False)

category = valid.groupby("Category").agg(
    Observed_Sales_INR=("Discounted_Sales_INR", "sum"),
    Transactions=("Transaction_ID", "count"),
).reset_index()
category.to_csv(OUT / "category_sales.csv", index=False)

retention.to_csv(OUT / "cohort_retention_pct.csv", index=False)

kpis = {
    "total_customers": int(customers["Customer_ID"].nunique()),
    "sales_transactions": int(len(sales)),
    "valid_transactions": int((~sales["Is_Returned"]).sum()),
    "observed_sales_inr": round(
        float(valid["Discounted_Sales_INR"].sum()), 2
    ),
    "average_observed_sales_per_customer_inr": round(
        float(valid["Discounted_Sales_INR"].sum())
        / max(customers["Customer_ID"].nunique(), 1), 2
    ),
    "churned_customers": int(customers["Churned"].sum()),
    "average_frequency": round(float(customers["Frequency"].mean()), 2),
    "average_recency_days": round(float(customers["Recency"].mean()), 2),
}

(OUT / "dashboard_kpis.json").write_text(
    json.dumps(kpis, indent=2),
    encoding="utf-8",
)

print("WEEK 9 AGGREGATE DATA CREATED")
print(f"Output folder: {OUT}")
print(f"Customers represented: {kpis['total_customers']}")
print(f"Transactions represented: {kpis['sales_transactions']}")
print(f"Observed sales: INR {kpis['observed_sales_inr']:,.2f}")
print(f"Aggregate files: {len(list(OUT.glob('*')))}")
