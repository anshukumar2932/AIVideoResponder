import os
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import logging

from stt import speech_to_text
from src.predict_intent import predict_intent
from src.response_generator import generate_response
from tts import generate_audio

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        "status": "Customer Support AI Backend Running",
        "version": "1.0.0",
        "endpoints": ["/", "/text-support", "/support", "/video"]
    })


# ==============================
# Text Support Route (Render-friendly)
# ==============================
@app.route("/text-support", methods=["POST"])
def text_support():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"].strip()
    
    if not user_text:
        return jsonify({"error": "Empty text provided"}), 400

    try:
        logger.info(f"Processing text: {user_text}")
        
        # 1️⃣ Predict Intent
        intent = predict_intent(user_text)
        logger.info(f"Predicted intent: {intent}")

        # 2️⃣ Generate Response
        response_text = generate_response(intent)
        logger.info(f"Generated response: {response_text}")

        return jsonify({
            "user_text": user_text,
            "intent": intent,
            "response": response_text,
            "success": True
        })

    except Exception as e:
        logger.error(f"Error in text support: {str(e)}")
        return jsonify({"error": str(e), "success": False}), 500


# ==============================
# Audio Support Route (Simplified for Render)
# ==============================
@app.route("/support", methods=["POST"])
def customer_support():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    file_id = str(uuid.uuid4())
    audio_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.wav")
    
    try:
        file.save(audio_path)
        logger.info(f"Audio file saved: {audio_path}")

        # 1️⃣ Speech to Text
        user_text = speech_to_text(audio_path)
        logger.info(f"Speech to text result: {user_text}")

        if not user_text:
            return jsonify({"error": "No speech detected"}), 400

        # 2️⃣ Predict Intent
        intent = predict_intent(user_text)
        logger.info(f"Predicted intent: {intent}")

        # 3️⃣ Generate Response
        response_text = generate_response(intent)
        logger.info(f"Generated response: {response_text}")

        # 4️⃣ Text to Speech (Simplified)
        response_audio_path = f"response_{file_id}.mp3"
        try:
            generate_audio(response_text, response_audio_path)
            logger.info(f"Audio generated: {response_audio_path}")
        except Exception as audio_error:
            logger.warning(f"Audio generation failed: {audio_error}")
            response_audio_path = None

        # 5️⃣ For Render deployment, skip video generation due to ffmpeg requirements
        # Instead, return audio URL or fallback message
        video_available = False
        video_message = "Video generation is not available in this deployment environment."
        
        # Check if we're in a development environment
        if os.path.exists("/usr/bin/ffmpeg") or os.path.exists("/usr/local/bin/ffmpeg"):
            try:
                # Only attempt video generation if ffmpeg is available
                from generate_video import generate_video
                generate_video(response_text, response_audio_path, FINAL_VIDEO)
                video_available = True
                video_message = "Video generated successfully"
                logger.info("Video generated successfully")
            except Exception as video_error:
                logger.warning(f"Video generation failed: {video_error}")
                video_available = False
                video_message = f"Video generation failed: {str(video_error)}"

        # Clean up uploaded audio file
        try:
            os.remove(audio_path)
        except:
            pass

        response_data = {
            "user_text": user_text,
            "intent": intent,
            "response": response_text,
            "video_available": video_available,
            "video_message": video_message,
            "success": True
        }

        if video_available:
            response_data["video_url"] = "/video"
        
        if response_audio_path and os.path.exists(response_audio_path):
            response_data["audio_url"] = f"/audio/{file_id}"

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in customer support: {str(e)}")
        # Clean up files on error
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except:
            pass
        return jsonify({"error": str(e), "success": False}), 500


# ==============================
# Serve Generated Video (if available)
# ==============================
@app.route("/video")
def serve_video():
    if not os.path.exists(FINAL_VIDEO):
        return jsonify({
            "error": "Video not available", 
            "message": "Video generation is not supported in this deployment environment"
        }), 404

    try:
        return send_file(
            FINAL_VIDEO,
            mimetype="video/mp4",
            as_attachment=False
        )
    except Exception as e:
        logger.error(f"Error serving video: {str(e)}")
        return jsonify({"error": "Failed to serve video"}), 500


# ==============================
# Serve Generated Audio
# ==============================
@app.route("/audio/<file_id>")
def serve_audio(file_id):
    audio_path = f"response_{file_id}.mp3"
    
    if not os.path.exists(audio_path):
        return jsonify({"error": "Audio file not found"}), 404

    try:
        return send_file(
            audio_path,
            mimetype="audio/mpeg",
            as_attachment=False
        )
    except Exception as e:
        logger.error(f"Error serving audio: {str(e)}")
        return jsonify({"error": "Failed to serve audio"}), 500


# ==============================
# System Info Endpoint (for debugging)
# ==============================
@app.route("/system-info")
def system_info():
    import platform
    import sys
    
    info = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "environment": os.environ.get("RENDER", "local"),
        "ffmpeg_available": os.path.exists("/usr/bin/ffmpeg") or os.path.exists("/usr/local/bin/ffmpeg"),
        "files_in_directory": os.listdir("."),
        "upload_folder_exists": os.path.exists(UPLOAD_FOLDER)
    }
    
    return jsonify(info)


# ==============================
# Run App (Render Compatible)
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting server on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    app.run(host="0.0.0.0", port=port, debug=debug)