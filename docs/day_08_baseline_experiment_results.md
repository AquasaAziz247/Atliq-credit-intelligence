# Day 8: Baseline Experiment Results

## 1. Objective

Establish a reproducible majority-class baseline and compare it with Logistic Regression using five approved numeric features. This is an educational classification experiment on the supplied labels, not a validated future-default prediction system.

## 2. Data and dependencies

- Customer rows: 50,000
- Loan rows: 50,000
- Customer join: 50,000 matched rows, zero unmatched rows
- Target: `default`
- Target counts: False = 45,703; True = 4,297
- Positive-label prevalence: 8.594%
- Added dependency: `scikit-learn==1.9.1`
- Dependency verification: `python -m pip check` reported no broken requirements.

## 3. Approved initial features

- `age`
- `income`
- `number_of_dependants`
- `years_at_current_address`
- `bank_balance_at_application`

All five features were observed to be numeric and have zero missing values in the supplied data. Their availability at a verified prediction time has not been established.

## 4. Evaluation split

- Training set: 40,000 rows
- Held-out test set: 10,000 rows
- Split method: stratified random split
- Test fraction: 0.20
- Random state: 42
- Reproducibility check: repeated split indices and targets were identical.

The held-out test set was not used to select the diagnostic thresholds. Threshold diagnostics used a separate validation subset carved from the training set.

## 5. Dummy baseline results

| Metric | Result |
|---|---:|
| Accuracy | 0.9141 |
| Precision for positive class | 0.0000 |
| Recall for positive class | 0.0000 |
| F1 for positive class | 0.0000 |
| ROC-AUC | 0.5000 |

Confusion matrix, actual rows and predicted columns, with labels False then True:

```text
[[9141    0]
 [ 859    0]]
```

The majority-class baseline predicts every test row as False. Its accuracy is high because the target is imbalanced, but it detects none of the positive labels.

## 6. Logistic Regression results

The model used a `StandardScaler` and `LogisticRegression(max_iter=1000, random_state=42)` inside a scikit-learn Pipeline.

| Metric | Result |
|---|---:|
| Accuracy | 0.9141 |
| Precision for positive class | 0.0000 |
| Recall for positive class | 0.0000 |
| F1 for positive class | 0.0000 |
| ROC-AUC | 0.5624 |

Confusion matrix:

```text
[[9141    0]
 [ 859    0]]
```

At the default 0.50 threshold, Logistic Regression predicts every test row as False. Its ROC-AUC is above 0.50, indicating weak ranking discrimination on this held-out split, but this result alone does not establish a useful model.

## 7. Predicted probability diagnostic

On the held-out test set, Logistic Regression produced these probability summary values:

- Mean: 0.085726
- Median: 0.083516
- 75th percentile: 0.099343
- 90th percentile: 0.115334
- 95th percentile: 0.125396
- 99th percentile: 0.142240
- Maximum: 0.160619

All scores were below 0.50, explaining why no positive class was predicted at the default threshold. These test-set threshold counts were diagnostic only and were not used to choose a final threshold.

## 8. Training-validation threshold diagnostic

A validation set of 8,000 rows was carved from the 40,000-row training partition. The remaining 32,000 rows were used to fit Logistic Regression. The 10,000-row held-out test set remained reserved.

| Threshold | Precision | Recall | F1 | Predicted positives |
|---:|---:|---:|---:|---:|
| 0.050 | 0.0871 | 0.9913 | 0.1602 | 7,827 |
| 0.075 | 0.0994 | 0.7689 | 0.1761 | 5,321 |
| 0.100 | 0.1063 | 0.2936 | 0.1560 | 1,901 |
| 0.125 | 0.1414 | 0.0799 | 0.1021 | 389 |
| 0.150 | 0.2500 | 0.0029 | 0.0057 | 8 |

Threshold 0.075 had the highest F1 among the five tested candidates on this validation split. It is not established as the globally optimal or operationally appropriate threshold. No operational cost function or decision requirement has been defined.

## 9. Interpretation

1. The majority-class baseline achieves 91.41% accuracy while having zero positive-class recall.
2. Logistic Regression has the same default-threshold classification metrics as the dummy baseline.
3. Logistic Regression has ROC-AUC 0.5624 on the held-out test set, suggesting weak ranking discrimination.
4. Lower thresholds can increase positive-label recall but produce many positive predictions and low precision.
5. Accuracy alone is inadequate for this imbalanced target.

## 10. Limitations and unresolved evidence

- The semantic definition of `default` is unverified.
- The target's observation window and label maturity are unverified.
- Feature availability at a verified prediction time is unverified.
- The split is random rather than temporal.
- The data may not represent a production lending population.
- No claim of validated future-default prediction, causal interpretation, or production readiness is supported.
- The threshold diagnostic tested only five candidate values and is exploratory.

## 11. Test status

After adding baseline module tests, the test suite reported:

```text
36 passed in 2.58s
```

The experiment module compiled successfully before execution. Actual metrics are recorded above from the observed console output.

## 12. Day 8 decision

The educational baseline comparison is complete. Keep the DummyClassifier as a reference and treat Logistic Regression as a preliminary candidate with weak discrimination and no positive predictions at the default threshold.

Before any broader model claims, resolve target meaning and feature timing where authoritative evidence is available. Do not add more complex models merely to improve apparent scores. Preserve the held-out test set for final evaluation and document any future experiment separately.
