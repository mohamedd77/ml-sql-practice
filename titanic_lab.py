import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("titanic.csv")

print(df.shape)
print(df.isna().sum()[df.isna().sum() > 0])
print(df.groupby("Sex")["Survived"].mean().round(2))
print(df.groupby("Pclass")["Survived"].mean().round(2))

num_cols = ["Age", "SibSp", "Parch", "Fare", "Pclass"]
cat_cols = ["Sex", "Embarked"]
X = df[num_cols + cat_cols]
y = df["Survived"]

numeric = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])
categorical = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])
prep = ColumnTransformer([
    ("num", numeric, num_cols),
    ("cat", categorical, cat_cols),
])

models = {
    "Baseline (always majority)": DummyClassifier(strategy="most_frequent"),
    "LogReg": LogisticRegression(max_iter=1000),
    "Forest": RandomForestClassifier(n_estimators=200, random_state=42),
}

for name, clf in models.items():
    pipe = Pipeline([("prep", prep), ("model", clf)])
    scores = cross_val_score(pipe, X, y, cv=5)
    print(f"{name}: mean {scores.mean():.3f}  std {scores.std():.3f}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
best = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])
best.fit(X_train, y_train)
print(classification_report(y_test, best.predict(X_test), target_names=["died", "survived"]))
