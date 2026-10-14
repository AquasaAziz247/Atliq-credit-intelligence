# AtliQ Credit Intelligence

An educational credit-risk analytics and machine-learning portfolio project focused on data quality, exploratory analysis, feature availability, and leakage prevention.

> **Project status:** Data audit, initial EDA, and preliminary feature-risk investigation are complete. Target semantics and feature collection timing remain unresolved. No model has been trained.

## Objectives

- Audit customer, loan, and bureau datasets.
- Explore loan and default-label patterns.
- Document suspicious records and unresolved data-quality questions.
- Assess whether candidate features could be available at the proposed prediction point.
- Develop reproducible, tested preprocessing utilities.
- Establish a defensible foundation for any later modeling.

## Technology

- Python
- pandas
- NumPy
- Plotly
- pytest
- Git

## Project structure

```text
atliq-credit-intelligence/
├── data/
│   └── raw/                 # Local source CSV files; not committed
├── docs/
│   └── day_03_decision_log.md
├── notebooks/
│   ├── day_02_eda.ipynb
│   └── day_03_feature_engineering_leakage_audit.ipynb
├── reports/
│   └── data_audit.txt
├── src/
│   ├── audit_data.py
│   ├── eda.py
│   └── preprocessing.py
├── tests/
│   └── test_preprocessing.py
├── requirements.txt
└── README.md
```

## Local setup

Use Python 3.13 or another Python version compatible with the pinned dependencies.

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The raw CSV files are not included in version control. Place the expected files in `data/raw/` before running the audit and EDA scripts.

## Run the audit

```powershell
python src/audit_data.py
```

## Run tests

```powershell
python -m pytest -v
```

## Data findings

The supplied dataset contains 50,000 customer records, 50,000 loan records, and 50,000 bureau records.

The loan table contains 4,297 records labeled `default = True`, representing 8.594% of the supplied labels.

Initial investigations identified:

- 62 missing `residence_type` values.
- 8 records with zero loan amounts and `principal_outstanding = -1`.
- 7 records where `processing_fee` exceeds a positive `loan_amount`.
- 1,840 records where `principal_outstanding` equals 5,000,000.
- An observed relationship in which all 50,000 `net_disbursement` values match 80% of `loan_amount` within 0.01.

These are observations, not proof that the flagged records are erroneous or that the observed formula represents a real banking rule.

## Important limitations

The dataset's target-generation logic, default observation horizon, and feature timestamps are undocumented. The proposed prediction point is before loan approval or disbursement, but feature eligibility has not been verified.

Fields that may reflect post-decision or later account information will not be treated as valid predictors without supporting evidence. This project is an educational prototype, not a validated lending system.

## Current validation

The preprocessing utility has four passing tests covering flag generation, preservation of the input DataFrame, required-column validation, and edge cases.
