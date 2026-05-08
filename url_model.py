import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("train_url.csv")

# Target column
target = "Type"

# Labels
y = data[target]

# Features
X = data.drop(target, axis=1)

# Keep numeric only
X = X.select_dtypes(include=['int64', 'float64'])

# Save feature names
feature_names = X.columns.tolist()

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# Save model + feature names
joblib.dump((model, feature_names), "url.pkl")

print("Model saved successfully")