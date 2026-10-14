
import pandas as pd
import pytest

from src.preprocessing import flag_suspicious_loans


def test_flags_suspicious_records_without_changing_input():
    loans = pd.DataFrame(
        {
            "loan_id": ["L001", "L002", "L003"],
            "loan_amount": [0, 1000, 2000],
            "principal_outstanding": [-1, 500, 100],
            "processing_fee": [0, 100, 2500],
        }
    )
    original = loans.copy(deep=True)

    result = flag_suspicious_loans(loans)

    assert result["flag_zero_loan_amount"].tolist() == [
        True, False, False
    ]
    assert result["flag_negative_principal"].tolist() == [
        True, False, False
    ]
    assert result["flag_fee_exceeds_loan"].tolist() == [
        False, False, True
    ]

    # The original DataFrame must remain unchanged.
    pd.testing.assert_frame_equal(loans, original)

    # No records should be deleted.
    assert len(result) == len(loans)


def test_missing_required_column_raises_error():
    loans = pd.DataFrame(
        {
            "loan_id": ["L001"],
            "loan_amount": [1000],
            "principal_outstanding": [500],
        }
    )

    with pytest.raises(ValueError, match="processing_fee"):
        flag_suspicious_loans(loans)



def test_empty_dataframe_returns_empty_result_with_flags():
    loans = pd.DataFrame(
        columns=[
            "loan_id",
            "loan_amount",
            "principal_outstanding",
            "processing_fee",
        ]
    )

    result = flag_suspicious_loans(loans)

    assert result.empty
    assert "flag_zero_loan_amount" in result.columns
    assert "flag_negative_principal" in result.columns
    assert "flag_fee_exceeds_loan" in result.columns


def test_zero_loan_amount_is_not_flagged_as_fee_exceeding_loan():
    loans = pd.DataFrame(
        {
            "loan_id": ["L001"],
            "loan_amount": [0],
            "principal_outstanding": [-1],
            "processing_fee": [100],
        }
    )

    result = flag_suspicious_loans(loans)

    assert result.loc[0, "flag_zero_loan_amount"]
    assert result.loc[0, "flag_negative_principal"]
    assert not result.loc[0, "flag_fee_exceeds_loan"]
