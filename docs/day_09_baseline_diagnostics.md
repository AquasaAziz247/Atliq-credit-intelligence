# Day 9: Baseline Diagnostics and Experiment Plan

## 1. Scope

This report records validation-only diagnostics and feature-quality
checks for the educational AtliQ Bank Credit Intelligence project.

The target is the supplied `default` label. Its meaning, generation
process, observation window, maturity, and prediction-time alignment
remain unverified. These experiments do not validate a real-world
future-default model or support lending decisions.

## 2. Reproducibility and split

The dataset contains 50,000 rows. The approved feature allowlist is:

- `age`
- `income`
- `number_of_dependants`
- `years_at_current_address`
- `bank_balance_at_application`

The target is `default`. The existing split uses stratification and
random state 42. The reserved test partition contains 10,000 rows.
The validation diagnostic uses 32,000 fit rows and 8,000 validation
rows from the training partition.

The verified positive-label rates were approximately:
- Fit: 8.5938%
- Validation: 8.6000%
- Test: 8.5900%

The fit, validation, and test partitions had no overlapping rows
in the split verification.

## 3. Validation probability diagnostics

A Logistic Regression pipeline with StandardScaler was fitted on the
32,000-row fit partition and evaluated on the 8,000-row validation
partition.

- Validation ROC-AUC: 0.5817
- Positive class: `True`
- Positive class index: 1
- Minimum predicted probability: 0.034166
- Median predicted probability: 0.083830
- 95th percentile: 0.124605
- Maximum predicted probability: 0.154368

Mean predicted probability by supplied label:
- Label False: 0.085361
- Label True: 0.091460

The distributions overlap substantially. ROC-AUC indicates weak
ranking discrimination, not verified calibration.

### Validation threshold diagnostics

| Threshold | Predicted positive | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|
| 0.050 | 7,827 | 0.0871 | 0.9913 | 0.1602 |
| 0.075 | 5,321 | 0.0994 | 0.7689 | 0.1761 |
| 0.100 | 1,901 | 0.1063 | 0.2936 | 0.1560 |
| 0.125 | 389 | 0.1414 | 0.0799 | 0.1021 |
| 0.150 | 8 | 0.2500 | 0.0029 | 0.0057 |
| 0.500 | 0 | 0.0000 | 0.0000 | 0.0000 |

Among these tested thresholds, 0.075 produced the highest validation
F1. This is an exploratory result, not a production threshold choice.
Thresholds must not be selected using the reserved test partition.

## 4. Feature-quality findings

No missing values were found in the five approved features.

Observed ranges:
- Age: 18 to 70
- Income: 0 to 11,999,000
- Number of dependants: 0 to 5
- Years at current address: 1 to 31
- Bank balance at application: 0 to 7,846,643

Income has 8 zero values. Bank balance has 8 zero values. Their
meaning has not been established; do not automatically remove or
impute them without investigating the source semantics.

Feature-to-label correlations:
- Age: -0.070336
- Income: -0.020949
- Bank balance at application: -0.018382
- Number of dependants: -0.009443
- Years at current address: 0.004715

These are weak individual linear associations. Correlation alone
does not establish feature usefulness, causality, fairness, or
point-in-time safety.

## 5. Interpretation and limitations

The majority-class baseline's high accuracy is misleading because
the positive supplied label occurs in only about 8.6% of rows.
The baseline Logistic Regression also predicts no positive cases at
the default 0.50 threshold in the reported test evaluation.

The validation threshold results show a precision-recall trade-off:
lower thresholds find more positive labels but generate many
positive predictions. The supplied target's real-world meaning is
still unknown.

No feature has been certified as available at the actual prediction
time. No authoritative target definition, target-generation process,
or observation window has been established. Do not describe this
prototype as a validated credit-risk decision system.

## 6. Next experiment

Proposed single controlled experiment: compare Logistic Regression
with `class_weight="balanced"` against the existing baseline.

Keep the feature allowlist, split seed, fit/validation/test boundaries,
and evaluation procedure unchanged. Fit only on the fit partition.
Compare validation ROC-AUC, precision, recall, F1, confusion matrix,
and predicted-positive count at clearly stated thresholds.

Do not use the reserved test partition to choose the model or
threshold. Treat any changed probability scores cautiously because
class weighting can affect score interpretation. Do not claim
calibration or real-world risk validity from these diagnostics.

## 7. Project integrity

Raw CSV files must remain unchanged. Preserve unrelated working-tree
changes. Review the final diff and stage only explicitly approved
Day 9 files. Do not push unless explicitly requested.
