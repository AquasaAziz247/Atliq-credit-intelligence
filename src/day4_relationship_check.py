
"""Read-only Day 4 dataset relationship diagnostics."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

FILES = {
    "customers": RAW / "customers.csv",
    "loans": RAW / "loans.csv",
    "bureau": RAW / "bureau_data.csv",
}

KEYS = {
    "customers": "cust_id",
    "loans": "loan_id",
    "bureau": "cust_id",
}


def main() -> None:
    tables = {
        name: pd.read_csv(path)
        for name, path in FILES.items()
    }

    print("=== DATASET SCHEMAS ===")
    for name, df in tables.items():
        print(f"\n{name}: rows={len(df):,}, columns={len(df.columns)}")
        print("Columns:", df.columns.tolist())
        print("Dtypes:")
        print(df.dtypes.to_string())

    print("\n=== KEY QUALITY ===")
    for name, key in KEYS.items():
        df = tables[name]
        print(f"\n{name}.{key}")
        if key not in df.columns:
            print("ERROR: required key column is missing")
            continue

        print(f"Rows: {len(df):,}")
        print(f"Missing key values: {df[key].isna().sum():,}")
        print(f"Distinct non-missing keys: {df[key].nunique():,}")
        print(f"Rows with duplicated key values: "
              f"{df[key].duplicated(keep=False).sum():,}")
        print(f"Extra occurrences beyond first per key: "
              f"{df[key].duplicated().sum():,}")

    print("\n=== CUSTOMER-LEVEL RELATIONSHIPS ===")
    customers = tables["customers"]
    loans = tables["loans"]
    bureau = tables["bureau"]

    for name, df in [("customers", customers), ("loans", loans),
                     ("bureau", bureau)]:
        if "cust_id" not in df.columns:
            raise ValueError(f"{name} is missing required key 'cust_id'")

    customer_ids = set(customers["cust_id"].dropna())
    loan_customer_ids = set(loans["cust_id"].dropna())
    bureau_customer_ids = set(bureau["cust_id"].dropna())

    print(f"Customer table rows: {len(customers):,}")
    print(f"Loan table rows: {len(loans):,}")
    print(f"Bureau table rows: {len(bureau):,}")
    print(f"Distinct customer IDs in customers: {len(customer_ids):,}")
    print(f"Distinct customer IDs in loans: {len(loan_customer_ids):,}")
    print(f"Distinct customer IDs in bureau: {len(bureau_customer_ids):,}")
    print("Distinct loan customer IDs absent from customers:",
          len(loan_customer_ids - customer_ids))
    print("Distinct bureau customer IDs absent from customers:",
          len(bureau_customer_ids - customer_ids))
    print("Distinct loan customer IDs absent from bureau:",
          len(loan_customer_ids - bureau_customer_ids))
    print("Distinct bureau customer IDs absent from loans:",
          len(bureau_customer_ids - loan_customer_ids))


    print("\n=== LOAN ID CHECK ===")
    if "loan_id" in loans.columns:
        print("Loan ID missing values:", loans["loan_id"].isna().sum())
        print("Distinct loan IDs:", loans["loan_id"].nunique())
        print("Duplicate loan ID rows:",
              loans["loan_id"].duplicated(keep=False).sum())
    else:
        raise ValueError("Loans table is missing required key 'loan_id'")

    print("\n=== LOANS PER CUSTOMER ===")
    loans_per_customer = loans.groupby("cust_id").size()

    print("Customers represented in loans:",
          len(loans_per_customer))
    print("Minimum loans per customer:",
          loans_per_customer.min())
    print("Maximum loans per customer:",
          loans_per_customer.max())
    print("Customers with multiple loans:",
          int((loans_per_customer > 1).sum()))

    print("\nLoan-count distribution:")
    print(
        loans_per_customer.value_counts()
        .sort_index()
        .to_string()
    )

    print("\n=== VALIDATED DIAGNOSTIC JOINS ===")
    print("These joins are temporary diagnostics only.")

    for name, right in [
        ("customers", customers),
        ("bureau", bureau),
    ]:
        print(f"\nLoans LEFT JOIN {name} on cust_id")

        try:
            joined = loans.merge(
                right,
                on="cust_id",
                how="left",
                validate="many_to_one",
                indicator=True,
            )

            print("Join validation: PASS (many_to_one)")
            print(f"Rows before: {len(loans):,}")
            print(f"Rows after: {len(joined):,}")
            print(
                "Matched loan rows:",
                int(joined["_merge"].eq("both").sum()),
            )
            print(
                "Unmatched loan rows:",
                int(joined["_merge"].eq("left_only").sum()),
            )
        except pd.errors.MergeError as exc:
            print("Join validation: FAILED")
            print(f"Reason: {exc}")

if __name__ == "__main__":
    main()
