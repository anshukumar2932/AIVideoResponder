import pickle
from sentence_transformers import SentenceTransformer


# Load trained classifier
with open("intent_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def predict_intent(user_text):
    embedding = embedder.encode([user_text])
    
    probs = model.predict_proba(embedding)[0]
    max_prob = max(probs)
    predicted_index = probs.argmax()
    
    intent = label_encoder.inverse_transform([predicted_index])[0]

    # Confidence threshold
    if max_prob < 0.55:
        return "uncertain"

    return intent


if __name__ == "__main__":
    while True:
        text = input("Enter text: ")
        print("Predicted Intent:", predict_intent(text))