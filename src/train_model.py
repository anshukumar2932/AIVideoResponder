# ==========================================
# 0️⃣ Imports
# ==========================================

import pandas as pd
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1️⃣ Load Dataset
# ==========================================

# Rename your dataset to dataset.csv for simplicity
DATASET_PATH = "dataset.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully.")
print("Total Samples:", len(df))
print("Unique Intents:", df["intent"].nunique())


# ==========================================
# 2️⃣ Text Preprocessing
# ==========================================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["cleaned_text"] = df["utterance"].apply(clean_text)

print("Text preprocessing completed.")


# ==========================================
# 3️⃣ Encode Intent Labels
# ==========================================

label_encoder = LabelEncoder()
df["intent_encoded"] = label_encoder.fit_transform(df["intent"])

print("Label encoding completed.")


# ==========================================
# 4️⃣ Train-Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    df["cleaned_text"],
    df["intent_encoded"],
    test_size=0.2,
    random_state=42,
    stratify=df["intent_encoded"]
)

# ==========================================
# 5️⃣ TF-IDF Vectorization
# ==========================================

vectorizer = TfidfVectorizer(
    analyzer='char_wb',
    ngram_range=(3,5),
    max_features=10000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("TF-IDF vectorization completed.")


# ==========================================
# 6️⃣ Train Logistic Regression Model
# ==========================================

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

print("Model training completed.")


# ==========================================
# 7️⃣ Evaluate Model
# ==========================================

y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)

print("\n==========================================")
print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("==========================================\n")

print("Classification Report:\n")
print(classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_
))


# ==========================================
# 8️⃣ Save Model Files
# ==========================================

with open("intent_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("\nModel files saved successfully.")
print("Training pipeline complete.")