
import csv
import json
from pathlib import Path
from collections import Counter
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"


def read_csv(filename):
    path = RAW / filename

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def to_number(value):
    return float(value.quantize(Decimal("0.01")))


def main():
    customers = read_csv("da_customer_profiles.csv")
    sales = read_csv("da_sales_transactions.csv")
    fintech = read_csv("da_fintech_transactions.csv")

    if not customers or not sales or not fintech:
        raise ValueError("One or more input datasets are empty.")

    customer_ids = {r["Customer_ID"] for r in customers}
    sales_ids = {r["Customer_ID"] for r in sales}

    if not sales_ids.issubset(customer_ids):
        raise ValueError("Sales contains customer IDs missing from profiles.")

    churned = sum(r["Churned"] == "1" for r in customers)
    total_revenue = sum(
        (Decimal(r["Total_Revenue"]) for r in customers), Decimal("0")
    )
    total_orders = sum(int(r["Total_Orders"]) for r in customers)

    gross = sum(
        (Decimal(r["Units"]) * Decimal(r["Unit_Price"]) for r in sales),
        Decimal("0"),
    )

    discounted = sum(
        (
            Decimal(r["Units"])
            * Decimal(r["Unit_Price"])
            * (1 - Decimal(r["Discount_Pct"]) / 100)
            for r in sales
        ),
        Decimal("0"),
    )

    non_returned = [r for r in sales if r["Return_Flag"] == "0"]

    non_returned_value = sum(
        (
            Decimal(r["Units"])
            * Decimal(r["Unit_Price"])
            * (1 - Decimal(r["Discount_Pct"]) / 100)
            for r in non_returned
        ),
        Decimal("0"),
    )

    statuses = Counter(r["status"] for r in fintech)
    successful = [r for r in fintech if r["status"] == "Success"]

    successful_amount = sum(
        (Decimal(r["amount_inr"]) for r in successful),
        Decimal("0"),
    )

    metrics = {
        "project": "PolicyBazaar Analytics",
        "scope": "Initial baseline; supplied sample data only",
        "customers": {
            "customer_count": len(customers),
            "average_profile_revenue_inr": to_number(
                total_revenue / len(customers)
            ),
            "average_profile_orders": to_number(
                Decimal(total_orders) / len(customers)
            ),
            "churned_customers": churned,
            "churn_rate_pct": to_number(
                Decimal(churned) / len(customers) * 100
            ),
        },
        "sales": {
            "transaction_count": len(sales),
            "gross_recorded_sales_inr": to_number(gross),
            "sales_after_discount_inr": to_number(discounted),
            "returned_records": len(sales) - len(non_returned),
            "non_returned_records": len(non_returned),
            "non_returned_sales_after_discount_inr": to_number(
                non_returned_value
            ),
        },
        "fintech": {
            "transaction_count": len(fintech),
            "status_counts": dict(sorted(statuses.items())),
            "successful_amount_inr": to_number(successful_amount),
            "fraud_flagged_records": sum(
                r["is_fraud"] == "1" for r in fintech
            ),
            "successful_fraud_flagged_records": sum(
                r["is_fraud"] == "1" for r in successful
            ),
        },
        "limitations": [
            "Only 200 customer profiles supplied, not the 50,000 target.",
            "Fintech user IDs have no verified mapping to Customer_ID.",
            "Sales data is not confirmed as insurance-policy revenue.",
            "These baselines are not validated insurance CLV metrics.",
        ],
    }

    REPORTS.mkdir(parents=True, exist_ok=True)

    json_path = REPORTS / "week3_baseline_metrics.json"
    json_path.write_text(
        json.dumps(metrics, indent=4, ensure_ascii=True),
        encoding="utf-8",
    )

    lines = [
        "# Week 3 - Baseline Metrics",
        "",
        "Generated reproducibly from the supplied raw CSV files.",
        "",
        "## Customer Profiles",
        f"- Customers: {metrics['customers']['customer_count']}",
        f"- Average profile revenue: INR {metrics['customers']['average_profile_revenue_inr']:.2f}",
        f"- Average orders: {metrics['customers']['average_profile_orders']:.2f}",
        f"- Churn rate: {metrics['customers']['churn_rate_pct']:.2f}%",
        "",
        "## Sales Transactions",
        f"- Transactions: {metrics['sales']['transaction_count']}",
        f"- Gross recorded sales: INR {metrics['sales']['gross_recorded_sales_inr']:.2f}",
        f"- Sales after discounts: INR {metrics['sales']['sales_after_discount_inr']:.2f}",
        f"- Returned records: {metrics['sales']['returned_records']}",
        f"- Non-returned records: {metrics['sales']['non_returned_records']}",
        f"- Non-returned sales after discounts: INR {metrics['sales']['non_returned_sales_after_discount_inr']:.2f}",
        "",
        "## Fintech Transactions",
        f"- Transactions: {metrics['fintech']['transaction_count']}",
        f"- Status counts: {metrics['fintech']['status_counts']}",
        f"- Successful amount: INR {metrics['fintech']['successful_amount_inr']:.2f}",
        f"- Fraud-flagged records: {metrics['fintech']['fraud_flagged_records']}",
        f"- Successful fraud-flagged records: {metrics['fintech']['successful_fraud_flagged_records']}",
        "",
        "## Data Limitations",
        *[f"- {item}" for item in metrics["limitations"]],
        "",
        "## Interpretation",
        "These are initial dataset baselines, not verified insurance revenue or CLV.",
        "Fintech amounts are reported separately because customer ID mapping is unavailable.",
        "Non-returned sales exclude records marked as returned; this is a proxy, not verified net revenue.",
        "",
    ]

    report_path = REPORTS / "week3_baseline_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print("PIPELINE COMPLETED")
    print(f"Customer profiles: {len(customers)}")
    print(f"Sales transactions: {len(sales)}")
    print(f"Fintech transactions: {len(fintech)}")
    print(f"JSON output: {json_path}")
    print(f"Report output: {report_path}")


if __name__ == "__main__":
    main()
