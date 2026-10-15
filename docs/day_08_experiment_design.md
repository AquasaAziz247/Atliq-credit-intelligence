# Day 8: Educational Experiment Design

## 1. Objective

Run a limited, reproducible educational classification experiment on the supplied binary `loans.default` label. The purpose is to practise baseline modeling, leakage-aware preprocessing, and honest evaluation.

This experiment is not a validated future-default prediction system and is not intended for real lending decisions.

## 2. Target definition and limitations

- Target column: `loans.default`.
- Observed target values: Boolean `False` and `True`.
- Previously observed counts: 45,703 False and 4,297 True, for 50,000 loan rows.
- The source target's business meaning, generation process, outcome window, assignment date, and maturity remain unverified.
- Do not invert, regenerate, or selectively remove target labels.
- Never include `default` in the predictor matrix.
- Model outputs must not be described as validated probabilities of future loan default.

## 3. Unit of analysis

Use one supplied loan row as one observation.

The inspected data showed 50,000 rows, 50,000 unique loan IDs, and 50,000 unique customer IDs. This supports one row per loan and one loan per customer in the supplied dataset. It does not establish that the same pattern holds in a broader lending population.

## 4. Initial numeric feature allowlist

The first educational experiment will use only these five numeric candidate fields:

- `age`
- `income`
- `number_of_dependants`
- `years_at_current_address`
- `bank_balance_at_application`

These features are selected for a narrow first experiment. Their names and data types do not prove that their definitions, reference dates, or values were available at a real-world prediction time. In particular, the timing and measurement method of `bank_balance_at_application` remain unverified.

Do not add other fields without updating and reviewing this document.

## 5. Exclusions

- `default`: target only, never a predictor.
- `cust_id` and `loan_id`: identifiers, not ordinary predictors.
- `gender`, `marital_status`, `employment_status`, and `residence_type`: excluded from the initial numeric-only experiment.
- `city`, `state`, and `zipcode`: excluded due to proxy, privacy, and generalization concerns.
- `loan_purpose`, `loan_type`, and loan amount/tenure fields: excluded from this first feature set; timing and business meaning are not sufficiently established.
- `principal_outstanding`, `processing_fee`, `gst`, and `net_disbursement`: excluded because they may reflect later account or lending-process information.
- All bureau fields: excluded until definitions, snapshot timing, and measurement windows are supported.
- `disbursal_date` and `installment_start_dt`: excluded from the initial predictors.

These exclusions apply to the initial experiment and do not imply that every excluded field is permanently unusable.

## 6. Evaluation split

- Split: stratified random train/test split.
- Training proportion: 80%.
- Test proportion: 20%.
- Random seed: 42.
- Stratify using the supplied target to preserve approximate class proportions in both partitions.
- Keep the test set isolated until final evaluation.
- Do not use test-set results to select features, tune models, or choose thresholds.
- A random split is an educational evaluation design, not a simulation of future deployment and not a remedy for unknown target semantics or feature timing.

## 7. Preprocessing policy

- Keep all raw CSV files unchanged.
- Fit any learned preprocessing only on the training partition.
- For the initial numeric-only experiment, inspect missingness and data types for the five selected features.
- If imputation or scaling is required, put the fitted transformations inside a scikit-learn pipeline.
- Do not fit transformations on the complete dataset before splitting.
- Do not silently delete rows or invent cleaning rules.
- Preserve and document observed anomalies.

## 8. Baseline sequence

1. Verify the schema, target, feature allowlist, and split behavior.
2. Implement a majority-class `DummyClassifier` baseline.
3. Review its held-out metrics.
4. Only then implement Logistic Regression in a leakage-aware pipeline.
5. Compare both models on the same held-out test partition.

No model has been trained as part of this design checkpoint.

## 9. Evaluation metrics

Report, where supported by actual outputs:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- ROC-AUC
- Average precision (PR-oriented metric)

State the positive-label convention and metric definitions. Accuracy alone is insufficient for a target with an observed positive proportion of 8.594%.

Metrics describe agreement with the supplied labels, not verified real-world defaults, credit losses, or successful default prevention.

## 10. Reproducibility and scope

- Random seed: 42.
- Preserve the exact feature list and split configuration in code and documentation.
- Add tests for feature/target separation, deterministic splitting, missing-value handling if applicable, and input schema.
- Record only results actually produced by the experiment.
- Do not copy metrics from the Codebasics reference notebook into this project.
- Do not claim production readiness or validated future-default prediction.

## 11. Unresolved evidence gaps

- Target meaning and generation process.
- Target observation window and label maturity.
- Intended real-world prediction timestamp.
- Reference dates and availability of candidate features.
- Measurement method and timestamp for `bank_balance_at_application`.

These gaps limit interpretation of the educational experiment and must remain visible in later reports.

## 12. Day 8 design decision

Proceed with the limited educational experiment under the assumptions documented above. Implement no model until this design is reviewed and the selected feature schema and missingness have been checked.
