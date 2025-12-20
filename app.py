from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from feature_extractor import extract_features

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("phishing_model.pkl")

@app.route("/")
def home():
    return "Phishing Detection API is running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # 🔑 Extract features (dict)
        features = extract_features(url)

        # 🔑 Convert dict → DataFrame (THIS IS THE FIX)
        df = pd.DataFrame([features])

        prediction = model.predict(df)[0]

        return jsonify({
            "phishing": int(prediction),
            "result": "PHISHING" if prediction == 1 else "SAFE"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
