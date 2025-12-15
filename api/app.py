from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import sys
import os
import pandas as pd

# Allow imports from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ML.feature_extractor import extract_features

app = Flask(__name__)
CORS(app)

# Load model once
model = joblib.load("ML/phishing_model.pkl")

@app.route("/check_url", methods=["POST"])
def check_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    try:
        features = extract_features(url)
        X = pd.DataFrame([features])
        prediction = model.predict(X)[0]
        print(X)

        return jsonify({
            "url": url,
            "phishing": bool(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)

