# phishing_detector.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from feature_extractor import extract_features
import joblib

# Load dataset
df = pd.read_csv("clean_dataset.csv")

# Extract features safely
feature_rows = []
label_rows = []

for index, row in df.iterrows():
    url = str(row["url"])
    status = row["status"].strip().lower()

    features = extract_features(url)
    feature_rows.append(features)
    label_rows.append(1 if status == "phishing" else 0)

X = pd.DataFrame(feature_rows)
y = pd.Series(label_rows)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model, "phishing_model.pkl")
print("Model saved as phishing_model.pkl")
