
"""Initial exploratory data analysis for AtliQ Credit Intelligence.

This script reads the original CSV files without modifying them.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px


# Resolve paths from this script's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Load the source datasets.
customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
loans = pd.read_csv(RAW_DATA_DIR / "loans.csv")
bureau = pd.read_csv(RAW_DATA_DIR / "bureau_data.csv")


def print_dataset_overview(name: str, df: pd.DataFrame) -> None:
    """Print a dataset's dimensions and column data types."""
    print(f"\n{'=' * 65}")
    print(f"DATASET: {name}")
    print("=" * 65)

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

    print("\nCOLUMN DATA TYPES")
    print(df.dtypes.to_string())


def print_feature_summaries(
    name: str,
    df: pd.DataFrame,
) -> None:
    """Summarise numerical and categorical features."""
    print(f"\n{'=' * 65}")
    print(f"FEATURE SUMMARIES: {name}")
    print("=" * 65)

    # Missing values
    missing = df.isna().sum()
    missing = missing[missing > 0]

    print("\nMISSING VALUES")
    if missing.empty:
        print("No missing values detected.")
    else:
        print(missing.to_string())
        print(f"Total missing cells: {int(missing.sum())}")

    # Numerical distributions
    numeric = df.select_dtypes(include="number")

    print("\nNUMERICAL SUMMARY")
    if numeric.empty:
        print("No numerical columns.")
    else:
        print(numeric.describe().round(2).to_string())

    # Categorical distributions
    categorical = df.select_dtypes(
        include=["object", "str", "category", "bool"]
    )

    print("\nCATEGORICAL VALUE COUNTS (top 10 per column)")

    for column in categorical.columns:
        # Avoid printing long lists of customer and loan identifiers.
        if column in {"cust_id", "loan_id"}:
            continue

        print(f"\n{column}:")
        print(
            categorical[column]
            .value_counts(dropna=False)
            .head(10)
            .to_string()
        )


def print_default_rates_by_category(
    df: pd.DataFrame,
    columns: list[str],
) -> None:
    """Report observed target rates for categorical groups."""
    print(f"\n{'=' * 65}")
    print("DEFAULT RATES BY CATEGORY")
    print("=" * 65)

    for column in columns:
        if column not in df.columns:
            print(f"\nSkipping {column}: column not found.")
            continue

        summary = (
            df.groupby(column, dropna=False)["default"]
            .agg(records="size", defaults="sum", default_rate="mean")
            .reset_index()
        )

        summary["default_rate_pct"] = (
            summary["default_rate"] * 100
        ).round(2)

        print(f"\n{column}:")
        print(
            summary[
                [column, "records", "defaults", "default_rate_pct"]
            ].to_string(index=False)
        )


def save_default_rate_chart(
    df: pd.DataFrame,
    category: str,
) -> None:
    """Save an interactive chart of observed default rates."""
    chart_data = (
        df.groupby(category, dropna=False)["default"]
        .agg(records="size", defaults="sum", default_rate="mean")
        .reset_index()
    )

    chart_data["default_rate_pct"] = (
        chart_data["default_rate"] * 100
    ).round(2)

    fig = px.bar(
        chart_data,
        x=category,
        y="default_rate_pct",
        text="default_rate_pct",
        hover_data=["records", "defaults"],
        title=f"Observed Default Rate by {category.replace('_', ' ').title()}",
        labels={
            category: category.replace("_", " ").title(),
            "default_rate_pct": "Observed Default Rate (%)",
            "records": "Number of Records",
            "defaults": "Number of Defaults",
        },
        template="plotly_white",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        yaxis_range=[0, max(20, chart_data["default_rate_pct"].max() * 1.2)],
        showlegend=False,
    )

    output_path = (
        PROJECT_ROOT / "reports" / "figures"
        / f"default_rate_by_{category}.html"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path)

    print(f"Chart saved: {output_path}")

def save_income_distribution_chart(df: pd.DataFrame) -> None:
    """Save an interactive histogram of customer income."""
    fig = px.histogram(
        df,
        x="income",
        nbins=50,
        title="Customer Income Distribution",
        labels={"income": "Annual Income"},
        template="plotly_white",
    )

    fig.update_layout(
        xaxis_title="Annual Income",
        yaxis_title="Number of Customers",
    )

    output_path = (
        PROJECT_ROOT / "reports" / "figures"
        / "customer_income_distribution.html"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path)

    print(f"Chart saved: {output_path}")

def save_income_by_default_chart(df: pd.DataFrame) -> None:
    """Save an interactive income distribution grouped by default status."""
    fig = px.histogram(
        df,
        x="income",
        color="default",
        nbins=50,
        barmode="overlay",
        opacity=0.65,
        title="Customer Income Distribution by Default Status",
        labels={
            "income": "Annual Income",
            "default": "Observed Default Status",
        },
        template="plotly_white",
    )

    fig.update_layout(
        xaxis_title="Annual Income",
        yaxis_title="Number of Records",
    )

    output_path = (
        PROJECT_ROOT / "reports" / "figures"
        / "customer_income_by_default.html"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path)

    print(f"Chart saved: {output_path}")    

def main() -> None:
    """Display the initial dataset and target overview."""
    print("ATLIQ CREDIT INTELLIGENCE")
    print("DAY 2: INITIAL EDA")
    print(f"Project root: {PROJECT_ROOT}")

    print_dataset_overview("customers.csv", customers)
    print_dataset_overview("loans.csv", loans)
    print_dataset_overview("bureau_data.csv", bureau)
    print_feature_summaries("customers.csv", customers)
    print_feature_summaries("loans.csv", loans)
    print_feature_summaries("bureau_data.csv", bureau)

    # Build an analysis-only table without changing the raw datasets.
    analysis = loans.merge(
        customers,      
        on="cust_id",
        how="left",
        validate="one_to_one",
    )

    analysis = analysis.merge(
        bureau,
        on="cust_id",
        how="left",
        validate="one_to_one",
    )

    print(f"\nMerged analysis shape: {analysis.shape}")
 
    print(f"\n{'=' * 65}")
    print("LOAN DEFAULT TARGET DISTRIBUTION")
    print("=" * 65)

    if "default" not in loans.columns:
        raise ValueError("Expected target column 'default' in loans.csv")

    target_counts = loans["default"].value_counts(dropna=False)
    target_percentages = loans["default"].value_counts(
        normalize=True,
        dropna=False,
    ).mul(100)

    target_summary = pd.DataFrame({
        "count": target_counts,
        "percentage": target_percentages,
    })

    
    print(target_summary.to_string())

    # Analyse observed default rates across categories.
    print_default_rates_by_category(
        analysis,
        [
            "loan_purpose",
            "loan_type",
            "gender",
            "employment_status",
            "residence_type",
        ],
    )

    save_default_rate_chart(analysis, "loan_purpose")
    save_default_rate_chart(analysis, "residence_type")
    save_income_distribution_chart(customers)
    save_income_by_default_chart(analysis)
    print("\nInitial EDA baseline completed.")



if __name__ == "__main__":
    main()
