from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from feature_extractor import extract_features

app = Flask(__name__)
CORS(app)

model = joblib.load("phishing_model.pkl")

@app.route("/", methods=["GET"])
def home():
    return {"status": "Phishing Detection API is live"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    features = extract_features(url)
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]

    return jsonify({
        "phishing": int(prediction),
        "result": "PHISHING" if prediction == 1 else "SAFE"
    })

if __name__ == "__main__":
      port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
