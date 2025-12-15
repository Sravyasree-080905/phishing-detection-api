import joblib
from feature_extractor import extract_features

# Load model
model = joblib.load("phishing_model.pkl")

print("\nPhishing Detection System Ready 🛡️\n")

while True:
    url = input("Enter URL (or type exit): ").strip()

    # Stop program
    if url.lower() in ["exit", "quit", "close"]:
        print("Exiting... Stay safe online! 💫")
        break

    # Empty input handling
    if url == "":
        print("❌ Empty input. Please enter a valid URL.")
        continue

    # Auto-correct missing http/https
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    try:
        features = extract_features(url)
        feature_list = [list(features.values())]

        prediction = model.predict(feature_list)[0]

        if prediction == 1:
            print("⚠️ Phishing\n")
        else:
            print("✔️ Legit\n")

    except Exception as e:
        print(f"⚠️ Error: {e}")
        print("❌ Could not process the URL.\n")
