# Day 12: Streamlit Prototype and Model Inference

## Objective

Create an initial Streamlit interface for the AtliQ Credit Intelligence educational credit-classification prototype and connect it to a reusable inference module.

## Implemented

- Added `src/model_inference.py` with a reusable baseline-model training function.
- Added input validation for required features, numeric values, non-finite values, and empty inputs.
- Added `tests/test_model_inference.py` with isolated inference tests.
- Created `app.py` as the Streamlit application entry point.
- Added a five-feature applicant form using the existing baseline feature list:
  - `age`
  - `income`
  - `number_of_dependants`
  - `years_at_current_address`
  - `bank_balance_at_application`
- Added an experimental positive-class probability display and a warning against interpreting it as validated future-default risk.
- Added Streamlit resource caching to avoid retraining the baseline model on every form submission.
- Pinned `streamlit==1.66.0` in `requirements.txt`.

## Verification Evidence

- Python syntax check for `app.py`: passed.
- Inference unit tests: 8 passed.
- Full project test suite after app integration and caching: 50 passed.
- Streamlit application launched locally and produced an experimental prediction in a manual smoke test.
- Example input shown during the smoke test returned a positive-class probability of 10.7%.

## Modeling and Safety Limitations

- The application is an educational prototype, not a validated lending or credit-scoring system.
- The displayed probability corresponds to the model's positive class for the existing dataset labels.
- It must not be presented as a calibrated probability of future loan default.
- The current feature set contains only the five baseline features.
- No new feature engineering, threshold tuning, or model selection was performed as part of this milestone.
- The inference model is trained from the established fit split. Validation and reserved test rows are not used by the inference training function.
- The reserved test partition must not be used for new model fitting or threshold selection.
- Model performance requirements have not been demonstrated as satisfied by this UI milestone.

## Git and Change Control

- Existing unrelated modification to `notebooks/day_02_eda.ipynb` must be preserved.
- Existing untracked file `src/audit_data_day1_backup.py` must be preserved.
- No commit or push has been performed for this milestone.

## Next Steps

1. Consider adding focused Streamlit interaction tests in a future iteration.
2. Consider adding explicit domain-range validation for inference inputs.
3. Keep target-definition and feature-timing limitations visible until supporting evidence is available.
4. Do not use the reserved test partition for new model fitting or threshold selection.
5. Obtain explicit approval before committing or pushing this milestone.
