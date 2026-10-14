
"""Apply Day 4 structural validation to the supplied CSV files."""

from pathlib import Path
import pandas as pd

from relationship_validation import (
    validate_key,
    validate_referential_integrity,
    validated_left_join,
    validate_binary_target,
)

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

customers = pd.read_csv(RAW / "customers.csv")
loans = pd.read_csv(RAW / "loans.csv")
bureau = pd.read_csv(RAW / "bureau_data.csv")

print("=== KEY VALIDATION ===")
validate_key(customers, "cust_id")
validate_key(loans, "loan_id")
validate_key(bureau, "cust_id")
print("PASS: required keys are present, non-missing, and unique.")

print("\n=== REFERENTIAL INTEGRITY ===")
validate_referential_integrity(loans, customers)
validate_referential_integrity(bureau, customers)
print("PASS: all loan and bureau customer IDs exist in customers.")

print("\n=== JOIN VALIDATION ===")
for name, right in [("customers", customers), ("bureau", bureau)]:
    joined = validated_left_join(loans, right)
    matched = int(joined["_merge"].eq("both").sum())
    unmatched = int(joined["_merge"].eq("left_only").sum())

    print(
        f"Loans LEFT JOIN {name}: "
        f"before={len(loans)}, after={len(joined)}, "
        f"matched={matched}, unmatched={unmatched}"
    )

print("\n=== TARGET STRUCTURE ===")
validate_binary_target(loans, "default")
print("PASS: default is present, complete, and binary.")
print("Observed label counts:")
print(loans["default"].value_counts().sort_index().to_string())

print("\n=== VALIDATION COMPLETE ===")
print("Structural validation does not establish target meaning or feature timing.")
