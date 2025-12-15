import sys
import os
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ML.feature_extractor import extract_features
from ui.blocker_popup import show_block_popup

model = joblib.load("ML/phishing_model.pkl")

url = sys.argv[1]

features = extract_features(url)
prediction = model.predict([list(features.values())])[0]

if prediction == 1:
    show_block_popup(url)
    print("⚠️ Phishing detected")
else:
    print("✔️ Legit website")
