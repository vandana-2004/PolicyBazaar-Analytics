import csv
from pathlib import Path
from datetime import date
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def read_csv(filename):
    with (RAW / filename).open(
        encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


def count_invalid(rows, condition):
    return sum(1 for row in rows if condition(row))


def main():
    customers = read_csv("da_customer_profiles.csv")
    sales = read_csv("da_sales_transactions.csv")
    fintech = read_csv("da_fintech_transactions.csv")

    datasets = [
        ("Customer Profiles", customers),
        ("Sales Transactions", sales),
        ("Fintech Transactions", fintech),
    ]

    print("POLICYBAZAAR ANALYTICS — WEEK 1 DATA QUALITY CHECK")
    print("=" * 58)

    for name, rows in datasets:
        missing = sum(
            1 for row in rows
            for value in row.values()
            if value is None or not value.strip()
        )
        duplicate_rows = len(rows) - len({
            tuple(row.items()) for row in rows
        })

        print(f"\n{name}")
        print(f"Rows: {len(rows)}")
        print(f"Columns: {len(rows[0]) if rows else 0}")
        print(f"Missing values: {missing}")
        print(f"Duplicate rows: {duplicate_rows}")

    print("\nPRIMARY KEY CHECKS")
    for label, rows, key in [
        ("Customer_ID", customers, "Customer_ID"),
        ("Transaction_ID", sales, "Transaction_ID"),
        ("txn_id", fintech, "txn_id"),
    ]:
        values = [row[key] for row in rows]
        print(f"{label} duplicates: {len(values) - len(set(values))}")

    date_issues = [
        row for row in customers
        if date.fromisoformat(row["First_Purchase_Date"])
        > date.fromisoformat(row["Last_Purchase_Date"])
    ]
    print("\nCUSTOMER DATE VALIDATION")
    print(f"Date-order inconsistencies: {len(date_issues)}")

    profile_ids = {row["Customer_ID"] for row in customers}
    sales_ids = {row["Customer_ID"] for row in sales}
    fintech_ids = {row["user_id"] for row in fintech}

    print("\nID LINKAGE")
    print(f"Unique profile IDs: {len(profile_ids)}")
    print(f"Unique sales customer IDs: {len(sales_ids)}")
    print(f"Sales IDs missing from profiles: {len(sales_ids - profile_ids)}")
    print(f"Fintech IDs matching profile IDs: {len(fintech_ids & profile_ids)}")

    checks = [
        ("Invalid Churned values", customers,
         lambda r: r["Churned"] not in {"0", "1"}),
        ("Negative Total_Orders", customers,
         lambda r: int(r["Total_Orders"]) < 0),
        ("Negative Total_Revenue", customers,
         lambda r: float(r["Total_Revenue"]) < 0),
        ("Invalid Return_Flag", sales,
         lambda r: r["Return_Flag"] not in {"0", "1"}),
        ("Non-positive Units", sales,
         lambda r: int(r["Units"]) <= 0),
        ("Non-positive Unit_Price", sales,
         lambda r: float(r["Unit_Price"]) <= 0),
        ("Discount outside 0-100", sales,
         lambda r: not 0 <= float(r["Discount_Pct"]) <= 100),
        ("Invalid is_weekend", fintech,
         lambda r: r["is_weekend"] not in {"0", "1"}),
        ("Invalid is_fraud", fintech,
         lambda r: r["is_fraud"] not in {"0", "1"}),
        ("Negative amount_inr", fintech,
         lambda r: float(r["amount_inr"]) < 0),
        ("Unexpected transaction status", fintech,
         lambda r: r["status"] not in {"Success", "Pending", "Failed"}),
    ]

    print("\nDOMAIN AND NUMERIC VALIDATION")
    for label, rows, condition in checks:
        print(f"{label}: {count_invalid(rows, condition)}")

    print("\nFINTECH STATUS COUNTS")
    for status, count in sorted(
        Counter(row["status"] for row in fintech).items()
    ):
        print(f"{status}: {count}")

    print("\nRAW DATA POLICY")
    print("Source files were read-only; no data was modified.")
    print("\nCheck completed.")


if __name__ == "__main__":
    main()
