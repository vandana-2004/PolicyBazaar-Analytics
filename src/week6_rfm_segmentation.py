import json
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "reports" / "week6"
CHARTS = OUT / "charts"

OBSERVATION_DATE = pd.Timestamp("2026-06-29")
RANDOM_STATE = 42
TARGET_CLUSTERS = 5


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)

    customers = pd.read_csv(
        RAW / "da_customer_profiles.csv"
    )
    sales = pd.read_csv(
        RAW / "da_sales_transactions.csv"
    )

    # Validate identifiers
    if customers["Customer_ID"].duplicated().any():
        raise ValueError("Duplicate customer profile IDs.")

    if sales["Transaction_ID"].duplicated().any():
        raise ValueError("Duplicate transaction IDs.")

    if not set(sales["Customer_ID"]).issubset(
        set(customers["Customer_ID"])
    ):
        raise ValueError("Unmatched sales customer IDs.")

    # Prepare transaction data
    sales["Date"] = pd.to_datetime(
        sales["Date"], errors="raise"
    )

    numeric_columns = [
        "Units", "Unit_Price", "Discount_Pct"
    ]

    for col in numeric_columns:
        sales[col] = pd.to_numeric(
            sales[col], errors="raise"
        )

    if not sales["Return_Flag"].isin([0, 1]).all():
        raise ValueError("Invalid Return_Flag values.")

    if (sales[numeric_columns[:2]] <= 0).any().any():
        raise ValueError("Invalid units or unit price.")

    if not sales["Discount_Pct"].between(0, 100).all():
        raise ValueError("Invalid discount percentage.")

    sales["Gross_Amount"] = (
        sales["Units"] * sales["Unit_Price"]
    )

    sales["Discounted_Amount"] = (
        sales["Gross_Amount"]
        * (1 - sales["Discount_Pct"] / 100)
    )

    # RFM uses non-returned transactions only.
    valid = sales[sales["Return_Flag"] == 0].copy()

    if valid.empty:
        raise ValueError("No non-returned transactions.")

    rfm = valid.groupby("Customer_ID").agg(
        Last_Purchase=("Date", "max"),
        Frequency=("Transaction_ID", "nunique"),
        Monetary=("Discounted_Amount", "sum")
    ).reset_index()

    rfm["Recency"] = (
        OBSERVATION_DATE - rfm["Last_Purchase"]
    ).dt.days

    if (rfm["Recency"] < 0).any():
        raise ValueError("Future transaction dates detected.")

    # Preserve customers without eligible purchases.
    rfm = customers[["Customer_ID"]].merge(
        rfm, on="Customer_ID", how="left"
    )

    # Attach profile attributes for interpretation.
    profile_columns = [
        "Customer_ID", "City", "Age_Band",
        "Gender", "Acquisition_Channel", "Churned"
    ]

    rfm = rfm.merge(
        customers[profile_columns],
        on="Customer_ID",
        how="left",
        validate="one_to_one"
    )

    rfm["Eligible_For_Clustering"] = (
        rfm["Recency"].notna()
        & (rfm["Frequency"] > 0)
        & (rfm["Monetary"] > 0)
    )

    rfm.to_csv(
        OUT / "rfm_customer_metrics.csv",
        index=False
    )

    # Prepare eligible records for clustering.
    model_data = rfm.loc[
        rfm["Eligible_For_Clustering"],
        ["Recency", "Frequency", "Monetary"]
    ].copy()

    if len(model_data) < 6:
        raise ValueError(
            "Insufficient eligible customers for clustering."
        )

    # Log transformation reduces monetary skew.
    transformed = np.log1p(model_data)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(transformed)

    # Evaluate multiple cluster counts.
    evaluations = []

    max_k = min(8, len(model_data) - 1)

    for k in range(2, max_k + 1):
        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=20
        )

        labels = model.fit_predict(scaled)

        score = silhouette_score(scaled, labels)

        evaluations.append({
            "k": k,
            "inertia": float(model.inertia_),
            "silhouette_score": float(score),
            "silhouette_pct": float(score * 100)
        })

    best = max(
        evaluations,
        key=lambda item: item["silhouette_score"]
    )

    # Evaluate the client's requested five-cluster solution.
    five_result = next(
        (item for item in evaluations if item["k"] == 5),
        None
    )

    if five_result is None:
        raise ValueError("Five-cluster model unavailable.")

    final_model = KMeans(
        n_clusters=TARGET_CLUSTERS,
        random_state=RANDOM_STATE,
        n_init=20
    )

    final_labels = final_model.fit_predict(scaled)

    rfm["Segment"] = pd.Series(
        pd.NA, index=rfm.index, dtype="Int64"
    )

    eligible_indices = rfm.index[
        rfm["Eligible_For_Clustering"]
    ]

    rfm.loc[eligible_indices, "Segment"] = (
        final_labels
    )

    rfm.to_csv(
        OUT / "customer_segments.csv",
        index=False
    )

    # Segment-level business profiles.
    profiles = rfm.loc[
        rfm["Eligible_For_Clustering"]
    ].groupby("Segment").agg(
        Customer_Count=("Customer_ID", "count"),
        Avg_Recency_Days=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Avg_Monetary_INR=("Monetary", "mean"),
        Median_Monetary_INR=("Monetary", "median"),
        Churn_Rate_Pct=("Churned", lambda x: x.mean() * 100)
    ).reset_index()

    profiles.to_csv(
        OUT / "segment_profiles.csv",
        index=False
    )

    # Evaluation results.
    results = {
        "project": "PolicyBazaar Analytics",
        "analysis": "Week 6 RFM and K-Means",
        "observation_date": str(
            OBSERVATION_DATE.date()
        ),
        "total_customers": int(len(customers)),
        "eligible_customers": int(len(model_data)),
        "excluded_customers": int(
            len(customers) - len(model_data)
        ),
        "observation_scope": (
            "Supplied sample sales data; "
            "not verified insurance policy data."
        ),
        "monetary_definition": (
            "Discounted value of non-returned transactions."
        ),
        "frequency_definition": (
            "Distinct non-returned sales transaction count."
        ),
        "recency_definition": (
            "Days since latest non-returned transaction."
        ),
        "requested_cluster_count": 5,
        "five_cluster_silhouette": five_result,
        "best_tested_model": best,
        "acceptance_target_silhouette_pct": 85,
        "target_met": (
            five_result["silhouette_pct"] >= 85
        ),
        "cluster_evaluations": evaluations
    }

    with (OUT / "cluster_evaluation.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(results, f, indent=4)

    # Plot silhouette scores.
    plt.figure(figsize=(9, 5))
    plt.plot(
        [x["k"] for x in evaluations],
        [x["silhouette_score"] for x in evaluations],
        marker="o"
    )
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("Silhouette score")
    plt.title("K-Means Cluster Evaluation")
    plt.xticks(range(2, max_k + 1))
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        CHARTS / "silhouette_evaluation.png",
        dpi=150
    )
    plt.close()

    # Segment size chart.
    plt.figure(figsize=(9, 5))
    profiles.plot(
        x="Segment",
        y="Customer_Count",
        kind="bar",
        legend=False
    )
    plt.title("Customer Distribution by Segment")
    plt.xlabel("Segment")
    plt.ylabel("Number of Customers")
    plt.tight_layout()
    plt.savefig(
        CHARTS / "segment_distribution.png",
        dpi=150
    )
    plt.close()

    # RFM distribution chart.
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    for ax, column in zip(
        axes, ["Recency", "Frequency", "Monetary"]
    ):
        ax.hist(
            model_data[column],
            bins=20,
            edgecolor="black"
        )
        ax.set_title(column)
        ax.set_ylabel("Customers")

    fig.suptitle("RFM Metric Distributions")
    fig.tight_layout()
    fig.savefig(
        CHARTS / "rfm_distributions.png",
        dpi=150
    )
    plt.close(fig)

    # Initial analytical report.
    report = [
        "# Week 6 — RFM Customer Segmentation",
        "",
        "## Scope",
        f"- Customer profiles: {len(customers)}",
        f"- Eligible customers: {len(model_data)}",
        f"- Excluded customers: {len(customers) - len(model_data)}",
        f"- Observation date: {OBSERVATION_DATE.date()}",
        "",
        "## RFM Methodology",
        "- Recency: days since last non-returned transaction.",
        "- Frequency: distinct non-returned transactions.",
        "- Monetary: discounted non-returned transaction value.",
        "- Monetary values are not confirmed insurance premiums.",
        "- Features were log-transformed and standardized.",
        "",
        "## K-Means Evaluation",
        f"- Requested clusters: 5",
        f"- Five-cluster silhouette: {five_result['silhouette_score']:.4f}",
        f"- Five-cluster silhouette percentage: {five_result['silhouette_pct']:.2f}%",
        f"- Best tested K: {best['k']}",
        f"- Best tested silhouette: {best['silhouette_score']:.4f}",
        f"- 85% target achieved: {results['target_met']}",
        "",
        "## Segment Profiles",
        profiles.to_string(index=False),
        "",
        "## Limitations",
        "- Only 200 customer profiles were supplied.",
        "- Sales data is not confirmed insurance-policy data.",
        "- Fintech records have no verified customer mapping.",
        "- The five-cluster solution requires business validation.",
        "- Silhouette score is a clustering metric, not prediction accuracy.",
        "- No validated future CLV target is available.",
        "",
        "## Interpretation",
        "These results describe the supplied sample dataset only.",
        "They must not be presented as validated insurance CLV findings."
    ]

    (OUT / "rfm_analysis_report.md").write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nWEEK 6 RFM ANALYSIS COMPLETED")
    print("Total customers:", len(customers))
    print("Eligible customers:", len(model_data))
    print("Excluded customers:",
          len(customers) - len(model_data))
    print("\nFive-cluster silhouette:",
          round(five_result["silhouette_score"], 4))
    print("Best tested K:", best["k"])
    print("Best silhouette:",
          round(best["silhouette_score"], 4))
    print("\nSEGMENT PROFILES")
    print(profiles.to_string(index=False))
    print("\nOUTPUT DIRECTORY:", OUT)


if __name__ == "__main__":
    main()
