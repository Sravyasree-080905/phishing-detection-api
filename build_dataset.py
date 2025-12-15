import pandas as pd
from feature_extractor import extract_features

# Load your original dataset (edit filename if needed)
df = pd.read_csv("dataset.csv")

# Your Excel MUST contain: URL, status
if "url" not in df.columns or "status" not in df.columns:
    raise ValueError("Excel must contain 'url' and 'status' columns!")

# Extract features for all URLs
rows = []
for url, status in zip(df["url"], df["status"]):
    try:
        features = extract_features(url)
        features["status"] = status
        rows.append(features)
    except:
        print("Skipping invalid URL:", url)

# Convert to dataframe
new_df = pd.DataFrame(rows)

# Save cleaned dataset
new_df.to_csv("clean_dataset.csv", index=False)

print("\n✨ New dataset created successfully!")
print("👉 File: clean_dataset.csv")
print("👉 Rows:", len(new_df))
print("👉 Columns:", list(new_df.columns))
