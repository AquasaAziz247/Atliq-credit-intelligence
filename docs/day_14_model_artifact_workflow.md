# Day 14: Local Model Artifact Workflow

## Objective

Separate model training from Streamlit prediction-time inference by generating a local serialized artifact from the established baseline training function.

## Implemented

- Added `src/model_artifact.py` with artifact generation, loading, and validation.
- Kept `train_inference_model()` in `src/model_inference.py` as the reproducible local training entry point used by the artifact generator.
- Added the command `python -m src.model_artifact`.
- The generator checks for `data/raw/customers.csv` and `data/raw/loans.csv`, then uses the existing training function and saves `models/baseline_inference_pipeline.joblib`.
- The loader uses `joblib`, verifies the expected scikit-learn `Pipeline` with `StandardScaler` and fitted `LogisticRegression`, and checks for the `True` positive class.
- Updated Streamlit to load the local artifact instead of fitting the model from raw CSV files during form submission.
- Added automated artifact tests using a synthetic fitted pipeline and temporary paths, without private source data.
- Pinned `joblib` explicitly in `requirements.txt`.
- Kept raw data and generated models excluded from Git through `.gitignore`.

## Local setup

From the repository root, with the project virtual environment active:

```powershell
python -m pip install -r requirements.txt
# Ensure data/raw/customers.csv and data/raw/loans.csv exist locally.
python -m src.model_artifact
python -m streamlit run app.py
```

The artifact is local and ignored by Git. Each development or hosting environment must generate or securely provide its own compatible artifact. The Streamlit app does not need raw CSV files at prediction time. If the artifact is missing, the app explains how to generate it.

## Preserved modeling design

No change was made to the approved feature list, `default` target, established fit/validation/reserved-test split, baseline Logistic Regression pipeline, thresholds, or historical experiment results. Artifact generation delegates training to the existing `train_inference_model()` function and fits only on the established fit partition.

## Limitations and security

- This is an educational classifier for the supplied labels, not a validated future-default risk model.
- Target-generation logic, outcome horizon, label maturity, and feature timestamps remain unresolved.
- The scorecard and probabilities are not validated or calibrated for real lending.
- Serialization does not improve predictive performance.
- Only load trusted joblib artifacts. Deserialization of an untrusted artifact can execute arbitrary code.
- Raw CSVs and model artifacts must not be committed or included in review archives.

## Verification record

Verification in the isolated review copy (Python 3.13.5, scikit-learn 1.8.0, joblib 1.5.3):

- Focused command `python -m pytest -q tests/test_model_artifact.py tests/test_model_inference.py tests/test_scorecard.py`: **42 passed**.
- Full command `python -m pytest -q`: **80 passed, 4 failed**. All four failures are in `tests/test_baseline_experiment.py` and require `data/raw/customers.csv`, which was intentionally excluded from the review archive. This is a data-dependent verification blocker, not a passing full-suite result.
- `python -m compileall -q app.py src tests`: passed.
- `python -m pip check`: failed due to an environment-level conflict: installed `moviepy 2.2.1` requires `pillow<12.0,>=9.2.0`, but the review environment has Pillow 12.3.0.
- Artifact generation against the real dataset and a live Streamlit smoke test were not run because the raw CSVs are not present in the review archive.
- `git diff --check` against the user's actual repository cannot be asserted from this archive because it does not include `.git` history. A text-level whitespace check is still required in the original working tree.

These are results from the isolated review copy, not from the user's original virtual environment. No commit, push, or deployment is part of this milestone.

## Change control

The pre-existing modification to `notebooks/day_02_eda.ipynb` and untracked `src/audit_data_day1_backup.py` were preserved in the supplied archive and are not intentionally edited by this workflow.
