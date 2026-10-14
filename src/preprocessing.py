
"""Read-only data-quality checks for AtliQ Credit Intelligence."""

import pandas as pd


def flag_suspicious_loans(loans: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of loan records with investigation flags.

    This function does not delete records, change source values, or infer
    that a flagged value is definitively incorrect.
    """
    required_columns = {
        "loan_id",
        "loan_amount",
        "principal_outstanding",
        "processing_fee",
    }

    missing_columns = required_columns.difference(loans.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    flagged = loans.copy()

    flagged["flag_zero_loan_amount"] = flagged["loan_amount"].eq(0)

    flagged["flag_negative_principal"] = (
        flagged["principal_outstanding"].lt(0)
    )

    flagged["flag_fee_exceeds_loan"] = (
        flagged["loan_amount"].gt(0)
        & flagged["processing_fee"].gt(flagged["loan_amount"])
    )

    return flagged
