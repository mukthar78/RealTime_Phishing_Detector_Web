import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("train_con.csv")

# =========================
# TARGET COLUMN
# =========================

y = data["status"]

# =========================
# FEATURES
# =========================

X = data.drop("status", axis=1)

# Keep only numeric columns
X = X.select_dtypes(include=['int64', 'float64'])

feature_names = X.columns.tolist()

# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# =========================
# MODEL
# =========================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# =========================
# TRAIN
# =========================

model.fit(X_train, y_train)

# =========================
# TEST
# =========================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# =========================
# SAVE
# =========================

joblib.dump(
    (model, feature_names),
    "con.pkl"
)

print("Model Saved")