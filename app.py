import os
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from src.stt import speech_to_text
from src.predict_intent import predict_intent
from src.response_generator import generate_response
from src.tts import speak
from src.generate_video import generate_video

app = Flask(__name__)
CORS(app)

# ==============================
# Config
# ==============================
UPLOAD_FOLDER = "uploads"
FINAL_VIDEO = "final.mp4"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==============================
# Health Check 
# ==============================
@app.route("/")
def home():
    return jsonify({
        "status": "Customer Support AI Backend Running"
    })


# ==============================
# Main Customer Support Route
# ==============================
@app.route("/support", methods=["POST"])
def customer_support():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]

    file_id = str(uuid.uuid4())
    audio_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.wav")
    file.save(audio_path)

    try:
        # 1️⃣ Speech to Text
        user_text = speech_to_text(audio_path)

        if not user_text:
            return jsonify({"error": "No speech detected"}), 400

        # 2️⃣ Predict Intent
        intent = predict_intent(user_text)

        # 3️⃣ Generate Response
        response_text = generate_response(intent)

        # 4️⃣ Text to Speech
        response_audio_path = speak(response_text)

        #  Generate Video
        generate_video(response_text, response_audio_path, FINAL_VIDEO)

        return jsonify({
            "user_text": user_text,
            "intent": intent,
            "response": response_text,
            "video_url": "/video"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==============================
# Serve Generated Video
# ==============================
@app.route("/video")
def serve_video():
    if not os.path.exists(FINAL_VIDEO):
        return jsonify({"error": "Video not generated yet"}), 404

    return send_file(
        FINAL_VIDEO,
        mimetype="video/mp4",
        as_attachment=False
    )


# ==============================
# Run App (Render Compatible)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)