# ML and SQL Practice

Small, runnable exercises on real data: SQL with sqlite3 and classic ML with scikit-learn.

## Contents
- `sql_lab.py`: SELECT, WHERE, ORDER BY, GROUP BY, inner and left JOIN, HAVING.
- `sql_lab2.py`: INSERT/UPDATE/DELETE, parameterized queries vs SQL injection, subqueries, indexes and query plans.
- `ml_lab.py`: breast cancer dataset (scikit-learn): Logistic Regression vs Random Forest, cross-validation, confusion matrix.
- `titanic_lab.py`, `titanic_lab2.py`: Titanic survival with imputation, one-hot encoding, ColumnTransformer, baseline, feature engineering, GridSearchCV.

## Run

## Results (5-fold cross-validation)
| Dataset | Model | Accuracy |
|---|---|---|
| Breast cancer | Logistic Regression | 0.981 |
| Breast cancer | Random Forest | 0.956 |
| Titanic | Baseline (majority class) | 0.616 |
| Titanic | Logistic Regression | 0.788 |
| Titanic | Random Forest | 0.807 |
| Titanic | Logistic Regression + FamilySize + Title | 0.826 |

## Notes
- A simple model beat the Random Forest on the small, clean breast cancer data.
- The Title feature (extracted from Name) helped more than a bigger model.
- The GridSearchCV score is optimistic because it is the best of several tries on the same folds. A held-out test set would be more honest.
- Data: the breast cancer dataset ships with scikit-learn. `titanic.csv` is the public Titanic passenger dataset.
