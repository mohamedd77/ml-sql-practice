import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

data = load_breast_cancer(as_frame=True)
df = data.frame
print(df.shape)
print(df["target"].value_counts())
print(data.target_names)

X = df.drop(columns="target")
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

logreg = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
forest = RandomForestClassifier(random_state=42)

for name, model in [("LogReg", logreg), ("Forest", forest)]:
    model.fit(X_train, y_train)
    print(name, "train:", round(model.score(X_train, y_train), 3),
          "test:", round(model.score(X_test, y_test), 3))
    cv = cross_val_score(model, X, y, cv=5)
    print(name, "5-fold CV: mean", round(cv.mean(), 3), "std", round(cv.std(), 3))

pred = logreg.predict(X_test)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred, target_names=data.target_names))

imp = pd.Series(forest.feature_importances_, index=X.columns).sort_values(ascending=False)
print(imp.head(5).round(3))
