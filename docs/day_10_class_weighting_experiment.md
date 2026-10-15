# Day 10: Class-Weighting Experiment

## 1. Objective

Compare the existing Logistic Regression baseline with Logistic Regression using `class_weight="balanced"` to understand how class weighting affects classification of an underrepresented positive class.

This is an educational experiment on supplied labels, not a validated future-default prediction system.

## 2. Experimental controls

- **Approved features:** `age`, `income`, `number_of_dependants`, `years_at_current_address`, `bank_balance_at_application`
- **Target:** `default`
- **Random state:** 42
- **Fit partition:** 32,000 rows
- **Validation partition:** 8,000 rows
- **Reserved test partition:** 10,000 rows
- **Fit positive-label rate:** 8.5938%
- **Validation positive-label rate:** 8.6000%
- **Preprocessing:** `StandardScaler` inside a scikit-learn pipeline
- **Models:** baseline Logistic Regression and Logistic Regression with `class_weight="balanced"`
- **Thresholds:** 0.50 and 0.075

Both models use the same fit and validation partitions, features, scaling approach, random state, and iteration limit. The reserved test partition is not used for model selection, threshold selection, or metric reporting.

## 3. Validation results

| Model    | Threshold | ROC-AUC | Precision | Recall |     F1 | Predicted positives | Proportion |
| -------- | --------: | ------: | --------: | -----: | -----: | ------------------: | ---------: |
| Baseline |     0.500 |  0.5817 |    0.0000 | 0.0000 | 0.0000 |                   0 |     0.0000 |
| Baseline |     0.075 |  0.5817 |    0.0994 | 0.7689 | 0.1761 |               5,321 |     0.6651 |
| Balanced |     0.500 |  0.5815 |    0.1035 | 0.5610 | 0.1748 |               3,729 |     0.4661 |
| Balanced |     0.075 |  0.5815 |    0.0860 | 1.0000 | 0.1584 |               8,000 |     1.0000 |

ROC-AUC measures ranking performance across thresholds. Precision, recall, F1, and the proportion classified positive depend on the threshold.

## 4. Confusion matrices

Rows are actual labels and columns are predicted labels, both ordered `[False, True]`.

### Baseline at threshold 0.50

```text
[[7312    0]
 [ 688    0]]
```

The model predicts every validation row as negative and misses all 688 positive labels.

### Baseline at threshold 0.075

```text
[[2520 4792]
 [ 159  529]]
```

It identifies 529 of 688 positive labels but produces 4,792 false positives.

### Balanced model at threshold 0.50

```text
[[3969 3343]
 [ 302  386]]
```

It identifies 386 positive labels and produces 3,343 false positives.

### Balanced model at threshold 0.075

```text
[[   0 7312]
 [   0  688]]
```

Every validation row is classified as positive. Recall is 1.0, but precision is only 0.0860. Perfect recall alone does not make this a useful classifier.

## 5. Interpretation

### Did class weighting improve ROC-AUC?

No. Baseline ROC-AUC was 0.5817, while the balanced model achieved 0.5815. The difference is 0.0002 in favour of the baseline. Both results indicate weak ranking performance.

### Did class weighting improve positive-class detection?

At threshold 0.50, the balanced model detected 386 positive labels, whereas the baseline detected none. However, it also generated 3,343 false positives.

### Which tested configuration had the highest F1?

The baseline at threshold 0.075 achieved the highest F1 among these four configurations: 0.1761, with precision 0.0994 and recall 0.7689.

This does not prove that 0.075 is globally optimal or suitable for real lending decisions.

### Why did the balanced model predict every row as positive at 0.075?

All its validation positive-class probabilities were at least 0.075. The result demonstrates why threshold selection must consider confusion matrices and the predicted-positive proportion, not recall alone.

### Why keep the test set reserved?

Using test results repeatedly to select models or thresholds would leak evaluation information into development decisions. Keep the test partition untouched until the modelling and evaluation plan are fixed.

## 6. Limitations and responsible use

- The target's business meaning, label-generation process, outcome window, and maturity remain unresolved.
- Point-in-time feature availability has not been certified.
- Structural data validation does not establish predictive validity.
- ROC-AUC is weak, and precision is low across the tested configurations.
- Thresholds were not selected using documented business costs.
- Probability calibration has not been established.
- These results do not justify deployment or real credit decisions.

## 7. Interview preparation

**Q: Why use `class_weight="balanced"`?**

It adjusts the training loss to give more weight to the minority class. This can change the learned decision boundary and improve minority-class detection, but it does not guarantee better ranking or overall performance.

**Q: Why did the baseline predict no positives at 0.50?**

Its predicted positive probabilities did not reach 0.50 on this validation partition. With an underrepresented positive class, the default threshold can lead to majority-class-only predictions.

**Q: Why report both ROC-AUC and F1?**

ROC-AUC measures ranking across thresholds, while F1 summarizes the precision-recall trade-off at a particular threshold. Neither metric captures every operational cost.

**Q: Why is 100% recall insufficient?**

Predicting every row as positive achieves perfect recall but can produce many false positives. Here, precision is only 0.0860.

**Q: Is the baseline at 0.075 ready for production?**

No. Ranking performance is weak, precision is low, and target meaning and feature timing remain unresolved.

## 8. Day 10 verification

- Dedicated class-weighting tests: 6 passed.
- Full project test suite: 42 passed.
- Data contract and relationship validation: passed.
- Dependency check: no broken requirements.
- Reserved test partition: not evaluated.
- Raw CSV files: not modified by this experiment.

Reproduce the experiment with:

```powershell
python -m src.class_weighting_experiment
```

Captured console output: `reports/day_10_class_weighting_results.txt`.

## 9. Day 11 recommendation

Do not add another model or perform broad hyperparameter tuning yet. Investigate target semantics, label generation, and feature availability at prediction time. Document unresolved assumptions and establish a defensible evaluation strategy before expanding the modelling work.
