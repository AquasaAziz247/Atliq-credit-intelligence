# Day 13: Educational Scorecard Integration

## Objective

Extend the AtliQ Credit Intelligence Streamlit prototype with an illustrative scorecard derived from the existing model's positive-class probability.

## Implemented

- Added `src/scorecard.py` with probability-to-score conversion and score-category mapping.
- Added `tests/test_scorecard.py` to validate score calculations, category boundaries, and invalid inputs.
- Integrated the scorecard into `app.py` while retaining the existing five-feature form and inference flow.
- Added an expandable explanation of the formula and category ranges.
- Preserved explicit warnings that the score and probability are experimental outputs.

## Score Formula

`S = round(900 - 600 * p)`

Here, `p` is the model's predicted probability for the positive class in the existing dataset labels.

| Score range | Category |
|---|---|
| 750–900 | Excellent |
| 650–749 | Good |
| 500–649 | Average |
| 300–499 | Poor |

The score is a custom educational transformation, not a validated or calibrated industry credit score.

## Verification Evidence

- Python compilation check for `app.py` and `src/scorecard.py`: passed.
- Scorecard tests: 29 passed.
- Focused scorecard and inference tests: 37 passed.
- Full project test suite: 79 passed.
- Manual Streamlit smoke test: interface loaded, an example prediction displayed, and the score explanation and limitations were visible.
- Example shown during the manual check: positive-class probability 10.7%, score 836, category Excellent.

## Limitations

- The score categories are custom prototype labels and must not be interpreted as evidence of creditworthiness.
- The positive-class probability is not a validated estimate of future loan default.
- The model's original performance requirements have not been demonstrated as satisfied.
- No new feature engineering, threshold tuning, or model selection was performed for this milestone.
- The target-generation logic, outcome horizon, and feature-timing limitations remain unresolved.
- No claim of production readiness or lending suitability is made.

## Git and Change Control

- Existing staged Day 12 changes must be preserved.
- The unrelated modification to `notebooks/day_02_eda.ipynb` and untracked file `src/audit_data_day1_backup.py` must be preserved.
- No commit or push has been performed for this milestone.

## Next Steps

1. Review the final diff and Git status.
2. Consider dedicated Streamlit interaction tests and domain-range validation.
3. Continue investigating target definition, outcome horizon, and feature timing.
4. Obtain explicit approval before committing or pushing.
