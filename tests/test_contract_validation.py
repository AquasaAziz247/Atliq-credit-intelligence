
import pandas as pd
import pytest

from src.contract_validation import (
    validate_dataset_contract,
    validate_missingness,
    validate_primary_key,
    validate_schema,
)
from src.data_contracts import CUSTOMER_COLUMNS


def valid_customers():
    """Return a minimal customer table satisfying the current contract."""
    return pd.DataFrame(
        {
            "cust_id": ["C001", "C002"],
            "age": [25, 40],
            "gender": ["F", "M"],
            "marital_status": ["Single", "Married"],
            "employment_status": ["Employed", "Employed"],
            "income": [30000, 60000],
            "number_of_dependants": [0, 2],
            "residence_type": ["Rented", None],
            "years_at_current_address": [2, 8],
            "city": ["Kolkata", "Kolkata"],
            "state": ["West Bengal", "West Bengal"],
            "zipcode": ["700001", "700002"],
        }
    )


def test_valid_customer_contract_passes():
    validate_dataset_contract(valid_customers(), "customers")



def test_empty_dataset_is_rejected():
    df = pd.DataFrame(columns=sorted(CUSTOMER_COLUMNS))

    with pytest.raises(ValueError, match="must not be empty"):
        validate_schema(df, "customers")



def test_missing_required_column_is_rejected():
    df = valid_customers().drop(columns=["income"])

    with pytest.raises(ValueError, match="missing required columns"):
        validate_schema(df, "customers")


def test_unknown_dataset_is_rejected():
    with pytest.raises(ValueError, match="Unknown dataset contract"):
        validate_schema(valid_customers(), "unknown")


def test_missing_primary_key_is_rejected():
    df = valid_customers().copy()
    df.loc[0, "cust_id"] = None

    with pytest.raises(ValueError, match="contains missing values"):
        validate_primary_key(df, "customers")


def test_duplicate_primary_key_is_rejected():
    df = valid_customers().copy()
    df.loc[1, "cust_id"] = df.loc[0, "cust_id"]

    with pytest.raises(ValueError, match="contains duplicate values"):
        validate_primary_key(df, "customers")


def test_undocumented_missingness_is_rejected():
    df = valid_customers().copy()
    df.loc[0, "income"] = None

    with pytest.raises(ValueError, match="unexpected missing values"):
        validate_missingness(df, "customers")


def test_documented_residence_type_missingness_is_allowed():
    df = valid_customers()

    validate_missingness(df, "customers")
