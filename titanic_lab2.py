import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("titanic.csv")

df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
df["Title"] = df["Name"].str.extract(r",\s*([^.]+)\.", expand=False).str.strip()
rare = df["Title"].value_counts()[lambda s: s < 10].index
df["Title"] = df["Title"].replace(rare, "Rare")
print(df["Title"].value_counts())

def build(num_cols, cat_cols, model):
    numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categorical = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    prep = ColumnTransformer([("num", numeric, num_cols), ("cat", categorical, cat_cols)])
    return Pipeline([("prep", prep), ("model", model)])

y = df["Survived"]
setups = {
    "base": (["Age", "SibSp", "Parch", "Fare", "Pclass"], ["Sex", "Embarked"]),
    "+FamilySize": (["Age", "SibSp", "Parch", "Fare", "Pclass", "FamilySize"], ["Sex", "Embarked"]),
    "+FamilySize+Title": (["Age", "SibSp", "Parch", "Fare", "Pclass", "FamilySize"], ["Sex", "Embarked", "Title"]),
}
for name, (nc, cc) in setups.items():
    X = df[nc + cc]
    for mname, m in [("LogReg", LogisticRegression(max_iter=1000)),
                     ("Forest", RandomForestClassifier(n_estimators=200, random_state=42))]:
        s = cross_val_score(build(nc, cc, m), X, y, cv=5)
        print(f"{name:20s} {mname:7s} mean {s.mean():.3f} std {s.std():.3f}")

nc, cc = setups["+FamilySize+Title"]
X = df[nc + cc]
pipe = build(nc, cc, RandomForestClassifier(random_state=42))
grid = GridSearchCV(pipe, {"model__max_depth": [3, 5, 8, None],
                           "model__n_estimators": [100, 300]}, cv=5)
grid.fit(X, y)
print("best params:", grid.best_params_)
print("best CV:", round(grid.best_score_, 3))
