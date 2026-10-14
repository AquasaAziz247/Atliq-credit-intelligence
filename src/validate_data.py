
"""Run reproducible structural validation on all source datasets."""

from pathlib import Path

import pandas as pd

from src.contract_validation import validate_dataset_contract
from src.relationship_validation import (
    validate_binary_target,
    validate_referential_integrity,
    validated_left_join,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    customers = pd.read_csv(RAW_DATA / "customers.csv")
    loans = pd.read_csv(RAW_DATA / "loans.csv")
    bureau = pd.read_csv(RAW_DATA / "bureau_data.csv")

    datasets = {
        "customers": customers,
        "loans": loans,
        "bureau": bureau,
    }

    print("=== DATA CONTRACTS ===")
    for name, df in datasets.items():
        validate_dataset_contract(df, name)
        print(f"PASS: {name}, rows={len(df)}, columns={len(df.columns)}")

    print("\n=== RELATIONSHIP VALIDATION ===")
    validate_referential_integrity(loans, customers)
    validate_referential_integrity(loans, bureau)
    print("PASS: all loan customer IDs exist in both parent tables")

    customers_joined = validated_left_join(loans, customers)
    bureau_joined = validated_left_join(loans, bureau)

    for name, joined in (
        ("customers", customers_joined),
        ("bureau", bureau_joined),
    ):
        matched = int(joined["_merge"].eq("both").sum())
        unmatched = int(joined["_merge"].eq("left_only").sum())
        print(
            f"{name} join: rows={len(joined)}, "
            f"matched={matched}, unmatched={unmatched}"
        )

    print("\n=== TARGET STRUCTURE ===")
    validate_binary_target(loans, "default")
    print("PASS: default is non-empty, complete, and Boolean/integer binary")

    print("\nObserved target counts:")
    print(loans["default"].value_counts(dropna=False).sort_index())

    print("\n=== VALIDATION COMPLETE ===")
    print(
        "Structural validity does not establish target meaning, "
        "outcome window, or feature availability at prediction time."
    )


if __name__ == "__main__":
    main()
