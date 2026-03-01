# AIVideoResponder Backend

Flask API for AI-powered customer support with video generation.

## 🚀 Quick Start

### Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server runs on `http://localhost:5000`

### Deploy to Fly.io
```bash
fly launch --name aivideo-backend
fly deploy
```

## 📡 API Endpoints

- `GET /` - Health check
- `POST /text-support` - Text-based support
- `POST /support` - Audio-based support (with video)
- `GET /video` - Serve generated video
- `GET /system-info` - System information

## 🔧 Environment Variables

- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Environment (production/development)

## 📦 Dependencies

- Flask - Web framework
- Whisper - Speech recognition
- Sentence Transformers - Intent classification
- Edge TTS - Text-to-speech
- FFmpeg - Video processing

## 🐳 Docker

Built with Dockerfile for Fly.io deployment with FFmpeg support.
