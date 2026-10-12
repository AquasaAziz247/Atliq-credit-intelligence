
"""Generate a reproducible audit of the raw AtliQ Bank datasets."""

from pathlib import Path

import pandas as pd


# Resolve paths from the project root, not the terminal's working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_PATH = REPORT_DIR / "data_audit.txt"

DATASETS = [
    "customers.csv",
    "loans.csv",
    "bureau_data.csv",
]


def audit_dataset(file_path: Path) -> list[str]:
    """Inspect one CSV file and return its audit findings."""

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    lines = [
        "=" * 72,
        f"DATASET: {file_path.name}",
        "=" * 72,
        f"Rows: {df.shape[0]:,}",
        f"Columns: {df.shape[1]:,}",
        "",
        "COLUMN DATA TYPES",
        "-" * 40,
        df.dtypes.to_string(),
        "",
        "MISSING VALUES",
        "-" * 40,
        df.isna().sum().to_string(),
        f"Total missing cells: {int(df.isna().sum().sum()):,}",
        "",
        "DUPLICATE ROWS",
        "-" * 40,
        f"Exact duplicate rows: {int(df.duplicated().sum()):,}",
        "",
        "NUMERIC SUMMARY",
        "-" * 40,
        df.describe(include="number").to_string(),
        "",
    ]

    if file_path.name == "loans.csv":
        lines.extend([
            "TARGET COLUMN CHECK",
            "-" * 40,
        ])

        if "default" in df.columns:
            lines.append("Target column 'default' found.")
            lines.append("Target value counts, including missing values:")
            lines.append(df["default"].value_counts(dropna=False).to_string())
            lines.append("")
            lines.append("Target proportions:")
            lines.append(
                df["default"].value_counts(
                    normalize=True, dropna=False
                ).to_string()
            )
        else:
            lines.append("WARNING: Target column 'default' not found.")

        lines.append("")

    return lines


def audit_relationships() -> list[str]:
    """Check identifier uniqueness and cross-table relationships."""

    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    loans = pd.read_csv(RAW_DATA_DIR / "loans.csv")
    bureau = pd.read_csv(RAW_DATA_DIR / "bureau_data.csv")

    lines = [
        "=" * 72,
        "RECORD INTEGRITY AND RELATIONSHIP AUDIT",
        "=" * 72,
        "",
    ]

    # Check identifier uniqueness and missing IDs.
    id_checks = [
        ("customers.csv", customers, "cust_id"),
        ("loans.csv", loans, "loan_id"),
        ("bureau_data.csv", bureau, "cust_id"),
    ]

    lines.append("IDENTIFIER QUALITY")
    lines.append("-" * 40)

    for filename, df, id_column in id_checks:
        missing_ids = int(df[id_column].isna().sum())
        duplicate_ids = int(df[id_column].duplicated().sum())

        lines.extend([
            f"{filename} | {id_column}",
            f"  Missing IDs: {missing_ids:,}",
            f"  Duplicate IDs: {duplicate_ids:,}",
            "",
        ])

    # Compare IDs across tables without modifying the source data.
    customer_ids = set(customers["cust_id"].dropna())
    loan_customer_ids = set(loans["cust_id"].dropna())
    bureau_customer_ids = set(bureau["cust_id"].dropna())

    orphan_loans = loan_customer_ids - customer_ids
    orphan_bureau = bureau_customer_ids - customer_ids

    lines.extend([
        "CROSS-TABLE RELATIONSHIPS",
        "-" * 40,
        f"Distinct customer IDs: {len(customer_ids):,}",
        f"Distinct loan customer IDs: {len(loan_customer_ids):,}",
        f"Distinct bureau customer IDs: {len(bureau_customer_ids):,}",
        f"Loan customer IDs absent from customers.csv: {len(orphan_loans):,}",
        f"Bureau customer IDs absent from customers.csv: {len(orphan_bureau):,}",
        "",
    ])

    # Check whether each loan has a corresponding bureau record.
    bureau_coverage = loan_customer_ids & bureau_customer_ids

    lines.extend([
        f"Loan customer IDs also present in bureau_data.csv: "
        f"{len(bureau_coverage):,}",
        "",
        "NOTE: Customer-level overlap does not prove that every loan has "
        "a corresponding point-in-time bureau record.",
        "",
    ])

    return lines


def audit_quality_flags() -> list[str]:
    """Flag suspicious values and validate loan date fields."""
    loans = pd.read_csv(RAW_DATA_DIR / "loans.csv")
    # Inspect negative outstanding balances without modifying the data.
    negative_balance_rows = loans.loc[
        loans["principal_outstanding"] < 0,
        [
            "loan_id",
            "cust_id",
            "loan_amount",
            "principal_outstanding",
            "disbursal_date",
            "installment_start_dt",
            "default",
        ],
    ]

    print("\nLoans with negative principal outstanding:")
    print(negative_balance_rows.to_string(index=False))


    lines = [
        "=" * 72,
        "DATA QUALITY FLAGS",
        "=" * 72,
        "",
    ]

    # Check values that may require domain-specific investigation.
    numeric_checks = {
        "principal_outstanding": lambda s: s < 0,
        "sanction_amount": lambda s: s < 0,
        "loan_amount": lambda s: s < 0,
        "processing_fee": lambda s: s < 0,
        "gst": lambda s: s < 0,
        "net_disbursement": lambda s: s < 0,
        "loan_tenure_months": lambda s: s <= 0,
        "bank_balance_at_application": lambda s: s < 0,
    }

    lines.append("NUMERIC VALUE FLAGS")
    lines.append("-" * 40)

    for column, condition in numeric_checks.items():
        flagged_count = int(condition(loans[column]).sum())
        lines.append(f"{column}: {flagged_count:,} flagged rows")

    lines.extend([
        "",
        "DATE VALIDATION",
        "-" * 40,
    ])

    date_columns = ["disbursal_date", "installment_start_dt"]

    for column in date_columns:
        parsed_dates = pd.to_datetime(
            loans[column],
            errors="coerce",
        )

        invalid_count = int(parsed_dates.isna().sum())

        lines.append(
            f"{column}: {invalid_count:,} unparseable or missing dates"
        )

    # Check chronology only when both dates can be parsed.
    disbursal = pd.to_datetime(
        loans["disbursal_date"],
        errors="coerce",
    )
    installment_start = pd.to_datetime(
        loans["installment_start_dt"],
        errors="coerce",
    )

    valid_pairs = disbursal.notna() & installment_start.notna()
    chronology_issues = int(
        (
            valid_pairs
            & (installment_start < disbursal)
        ).sum()
    )

    lines.append(
        "Installment starts before disbursal: "
        f"{chronology_issues:,} rows"
    )
    lines.append("")

    lines.append(
        "NOTE: Flags identify records for investigation; "
        "they do not establish that a value is incorrect."
    )
    lines.append("")
    lines.extend([
        "NEGATIVE BALANCE INVESTIGATION",
        "-" * 40,
        f"Flagged loan count: {len(negative_balance_rows):,}",
        "Flagged loan IDs: "
        + ", ".join(negative_balance_rows["loan_id"].tolist()),
        "Flagged rows with zero loan_amount: "
        + str(
            int((negative_balance_rows["loan_amount"] == 0).sum())
        ),
        "Interpretation: unresolved. The -1 value may be a sentinel, "
        "but dataset documentation is unavailable.",
        "",
    ])


    return lines



def main() -> None:
    """Audit all configured datasets and save one combined report."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_lines = [
        "ATLIQ CREDIT INTELLIGENCE",
        "RAW DATASET AUDIT REPORT",
        "Project root: .",
        "Datasets folder: data/raw",
        "",
    ]

    for filename in DATASETS:
        file_path = RAW_DATA_DIR / filename
        print(f"Auditing {filename}...")
        report_lines.extend(audit_dataset(file_path))


    report_lines.extend(audit_relationships())

    print("Checking identifiers and table relationships...")


    print("Checking numeric values and loan dates...")
    report_lines.extend(audit_quality_flags())

    report_text = "\n".join(report_lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")

    print("\nAudit completed.")
    print(f"Report saved to: {REPORT_PATH}")
    print("\n" + report_text)


if __name__ == "__main__":
    main()
