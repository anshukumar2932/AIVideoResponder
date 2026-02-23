# ==========================================
# 0️⃣ Imports
# ==========================================

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from sentence_transformers import SentenceTransformer


# ==========================================
# 1️⃣ Load Dataset
# ==========================================

DATASET_PATH = "dataset.csv"
df = pd.read_csv(DATASET_PATH)

print("Dataset Loaded Successfully.")
print("Total Samples:", len(df))
print("Unique Intents:", df["intent"].nunique())


# ==========================================
# 2️⃣ Label Encoding
# ==========================================

label_encoder = LabelEncoder()
df["intent_encoded"] = label_encoder.fit_transform(df["intent"])

print("Label encoding completed.")


##New Addition
print("Model Labels:")
print(label_encoder.classes_)

# ==========================================
# 3️⃣ Train-Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    df["utterance"],
    df["intent_encoded"],
    test_size=0.2,
    random_state=42,
    stratify=df["intent_encoded"]
)


# ==========================================
# 4️⃣ Load Embedding Model
# ==========================================

print("Loading SentenceTransformer model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded.")


# ==========================================
# 5️⃣ Generate Embeddings
# ==========================================

print("Generating embeddings...")

X_train_embeddings = embedder.encode(X_train.tolist(), show_progress_bar=True)
X_test_embeddings = embedder.encode(X_test.tolist(), show_progress_bar=True)

print("Embeddings generated.")


# ==========================================
# 6️⃣ Train Logistic Regression
# ==========================================

model = LogisticRegression(max_iter=1000)
model.fit(X_train_embeddings, y_train)

print("Model training completed.")


# ==========================================
# 7️⃣ Evaluation
# ==========================================

y_pred = model.predict(X_test_embeddings)
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
# 8️⃣ Save Model
# ==========================================

with open("intent_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("\nModel files saved successfully.")
print("Embedding-based training pipeline complete.")