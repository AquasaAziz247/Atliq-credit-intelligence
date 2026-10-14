
"""Read-only investigation of the candidate default target."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "data" / "raw" / "loans.csv"
loans = pd.read_csv(path)

print("=== TARGET COUNTS ===")
print(loans["default"].value_counts(dropna=False).to_string())
print(f"\nMissing target labels: {loans['default'].isna().sum()}")
print(f"Target dtype: {loans['default'].dtype}")
print(f"Unique target values: {loans['default'].unique().tolist()}")

print("\n=== DATE RANGES ===")
for column in ["disbursal_date", "installment_start_dt"]:
    dates = pd.to_datetime(loans[column], errors="coerce")
    print(f"\n{column}")
    print(f"Minimum date: {dates.min()}")
    print(f"Maximum date: {dates.max()}")
    print(f"Missing or unparseable: {dates.isna().sum()}")

print("\n=== SAMPLE LOAN RECORDS ===")
print(
    loans[
        ["loan_id", "disbursal_date", "installment_start_dt", "default"]
    ].head(10).to_string(index=False)
)

print("\n=== LABEL BY DISBURSAL YEAR ===")
loans["disbursal_date_parsed"] = pd.to_datetime(
    loans["disbursal_date"], errors="coerce"
)
loans["disbursal_year"] = loans["disbursal_date_parsed"].dt.year

print(
    loans.groupby("disbursal_year", dropna=False)["default"]
    .agg(records="size", positive_labels="sum", observed_rate="mean")
    .to_string()
)
