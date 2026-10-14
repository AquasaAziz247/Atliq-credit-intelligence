\# Day 5: Data Contracts and Modelling Readiness



\## Objective



Establish reusable structural data contracts, strengthen relationship and target validation, and provide a reproducible validation command for the AtliQ Credit Intelligence educational portfolio project.



\## Validation implementation



Added:

\- `src/data\_contracts.py`: expected source columns, primary keys, and currently documented missingness exceptions.

\- `src/contract\_validation.py`: reusable schema, missingness, and primary-key checks.

\- `src/validate\_data.py`: single entry point for validating all source tables, relationships, joins, and target structure.

\- `tests/test\_contract\_validation.py`: contract regression tests.



Updated:

\- `src/relationship\_validation.py`: rejects empty targets, invalid target values, missing join keys, empty relationship inputs, and duplicate parent keys during referential-integrity validation.

\- `tests/test\_relationship\_validation.py`: adds regression coverage for the discovered edge cases.



\## Verified results



\- Customers: 50,000 rows and 12 columns.

\- Loans: 50,000 rows and 15 columns.

\- Bureau: 50,000 rows and 8 columns.

\- All configured source contracts passed.

\- All loan customer IDs exist in both customers and bureau tables.

\- Both left joins preserved 50,000 rows and produced zero unmatched records.

\- `default` is non-empty, complete, and structurally Boolean/integer binary.

\- Observed labels: 45,703 False and 4,297 True.

\- Full test suite: 31 passed in 0.68 seconds.



Reproducible command:



`python -m src.validate\_data`



\## Known data-quality observations



\- `residence\_type` has 62 missing values in the current source data. The contract currently permits missingness in this column only.

\- Eight records have zero loan amounts with `principal\_outstanding = -1`.

\- Seven records have processing fees greater than loan amounts.

\- `principal\_outstanding` equals 5,000,000 in 1,840 records.

\- These observations require investigation and documented treatment before modelling. They must not be silently deleted or modified.



\## Target definition and prediction timing



The business definition of `default`, target-generation logic, outcome-observation window, and prediction horizon remain unverified.



A pre-approval or pre-disbursement prediction point has been considered as a provisional modelling assumption, not an established fact. Feature availability at that point remains to be confirmed.



Fields such as `principal\_outstanding`, `processing\_fee`, `gst`, and `net\_disbursement` are excluded from an initial candidate feature set pending timing verification. Identifiers are not predictors. The target must never be used as a feature.



\## Modelling-readiness decision



\*\*Status: structurally validated, not yet modelling-ready.\*\*



The source data passes the current structural contracts and relationship checks. This does not establish target validity, label maturity, leakage safety, or suitability for training a predictive model.



Before model training:

1\. Find authoritative documentation for the target definition and outcome window, or explicitly record that it is unavailable.

2\. Establish the intended prediction timestamp.

3\. Classify features by availability at that timestamp.

4\. Review data-quality anomalies and define a justified treatment.

5\. Select a validation strategy appropriate to the prediction setting and label timing.



No model has been trained as part of Day 5.



\## Scope and limitations



The contracts enforce the currently configured required columns, key constraints, and missingness policy. They do not yet validate every column's semantic meaning, numeric range, date validity, or business rules. Extra columns are permitted. A successful validation run must not be presented as proof of model readiness.
