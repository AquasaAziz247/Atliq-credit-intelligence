
import pandas as pd
import pytest

from src.relationship_validation import (
    validate_key,
    validate_referential_integrity,
    validated_left_join,
    validate_binary_target,
)


def test_validate_key_accepts_unique_non_missing_values():
    df = pd.DataFrame({"cust_id": ["C1", "C2"]})
    validate_key(df, "cust_id")


def test_validate_key_rejects_missing_column():
    with pytest.raises(ValueError, match="Missing required key"):
        validate_key(pd.DataFrame({"other": [1]}), "cust_id")


def test_validate_key_rejects_missing_values():
    df = pd.DataFrame({"cust_id": ["C1", None]})
    with pytest.raises(ValueError, match="missing values"):
        validate_key(df, "cust_id")


def test_validate_key_rejects_duplicates():
    df = pd.DataFrame({"cust_id": ["C1", "C1"]})
    with pytest.raises(ValueError, match="duplicate values"):
        validate_key(df, "cust_id")


def test_referential_integrity_accepts_matching_keys():
    child = pd.DataFrame({"cust_id": ["C1", "C2"]})
    parent = pd.DataFrame({"cust_id": ["C1", "C2", "C3"]})
    validate_referential_integrity(child, parent)


def test_referential_integrity_rejects_unmatched_key():
    child = pd.DataFrame({"cust_id": ["C1", "C9"]})
    parent = pd.DataFrame({"cust_id": ["C1", "C2"]})
    with pytest.raises(ValueError, match="absent from parent"):
        validate_referential_integrity(child, parent)


def test_validated_left_join_preserves_rows_and_reports_unmatched():
    left = pd.DataFrame({
        "cust_id": ["C1", "C2"],
        "amount": [100, 200],
    })
    right = pd.DataFrame({
        "cust_id": ["C1", "C3"],
        "segment": ["A", "B"],
    })

    joined = validated_left_join(left, right)

    assert len(joined) == len(left)
    assert joined["_merge"].tolist() == ["both", "left_only"]


def test_validated_left_join_rejects_duplicate_right_keys():
    left = pd.DataFrame({"cust_id": ["C1"]})
    right = pd.DataFrame({
        "cust_id": ["C1", "C1"],
        "segment": ["A", "B"],
    })

    with pytest.raises(pd.errors.MergeError):
        validated_left_join(left, right)


def test_binary_target_accepts_boolean_labels():
    df = pd.DataFrame({"default": [False, True, False]})
    validate_binary_target(df)


def test_binary_target_accepts_zero_one_labels():
    df = pd.DataFrame({"default": [0, 1, 0]})
    validate_binary_target(df)


def test_binary_target_rejects_missing_labels():
    df = pd.DataFrame({"default": [0, None]})
    with pytest.raises(ValueError, match="missing values"):
        validate_binary_target(df)


def test_binary_target_rejects_unexpected_values():
    df = pd.DataFrame({"default": [0, 2]})
    with pytest.raises(ValueError, match="only Boolean or integer 0/1"):
        validate_binary_target(df)


def test_binary_target_rejects_missing_target_column():
    with pytest.raises(ValueError, match="Missing target column"):
        validate_binary_target(pd.DataFrame({"other": [0, 1]}))


def test_binary_target_rejects_empty_dataframe():
    import pandas as pd
    import pytest

    from src.relationship_validation import validate_binary_target

    df = pd.DataFrame({"default": pd.Series([], dtype="bool")})

    with pytest.raises(ValueError, match="must not be empty"):
        validate_binary_target(df)


def test_binary_target_rejects_float_values():
    import pandas as pd
    import pytest

    from src.relationship_validation import validate_binary_target

    df = pd.DataFrame({"default": [0.0, 1.0]})

    with pytest.raises(ValueError, match="Boolean or integer 0/1"):
        validate_binary_target(df)


def test_binary_target_rejects_string_values():
    import pandas as pd
    import pytest

    from src.relationship_validation import validate_binary_target

    df = pd.DataFrame({"default": ["0", "1"]})

    with pytest.raises(ValueError, match="only Boolean or integer 0/1"):
        validate_binary_target(df)


def test_referential_integrity_rejects_duplicate_parent_keys():
    child = pd.DataFrame({"cust_id": ["C001"]})
    parent = pd.DataFrame({"cust_id": ["C001", "C001"]})

    with pytest.raises(ValueError, match="duplicate"):
        validate_referential_integrity(child, parent)


def test_validated_left_join_rejects_missing_left_keys():
    left = pd.DataFrame({"cust_id": [None], "loan_id": ["L001"]})
    right = pd.DataFrame({"cust_id": ["C001"], "income": [50000]})

    with pytest.raises(ValueError, match="missing"):
        validated_left_join(left, right)


def test_validated_left_join_rejects_missing_right_keys():
    left = pd.DataFrame({"cust_id": ["C001"], "loan_id": ["L001"]})
    right = pd.DataFrame({"cust_id": [None], "income": [50000]})

    with pytest.raises(ValueError, match="missing"):
        validated_left_join(left, right)