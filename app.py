from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

from feature_extractor import extract_features

app = Flask(__name__)
CORS(app)

model = joblib.load("phishing_model.pkl")

@app.route("/")
def home():
    return "Phishing Detection API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    features = extract_features(url)
    prediction = model.predict([features])[0]

    return jsonify({
        "url": url,
        "phishing": bool(prediction)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
