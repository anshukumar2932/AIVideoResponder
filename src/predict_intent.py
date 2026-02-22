import pickle
import re


# ----------------------------
# Load saved components
# ----------------------------

with open("intent_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)


# ----------------------------
# Text Cleaning (same as training)
# ----------------------------

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ----------------------------
# Predict Function
# ----------------------------

def predict_intent(user_text):
    cleaned = clean_text(user_text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    intent = label_encoder.inverse_transform([prediction])[0]
    return intent


# ----------------------------
# Standalone test
# ----------------------------

if __name__ == "__main__":
    while True:
        text = input("Enter text: ")
        print("Predicted Intent:", predict_intent(text))