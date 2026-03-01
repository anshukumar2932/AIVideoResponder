# AIVideoResponder

AI-powered customer support system that processes voice input and generates video responses with synchronized lip movements (visemes).

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Deployment

**Backend → Fly.io:**
```bash
cd backend
fly launch --name aivideo-backend
fly deploy
```

**Frontend → Vercel:**
1. Push code to GitHub
2. Import to Vercel: https://vercel.com/new
3. Set Root Directory: `frontend`
4. Add env var: `VITE_API_URL=https://aivideo-backend.fly.dev`

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📁 Project Structure

```
AIVideoResponder/
├── backend/              # Flask API (Fly.io)
│   ├── src/             # Core modules
│   ├── database/        # Database files
│   ├── dataset/         # Viseme videos
│   ├── app.py           # Main application
│   ├── Dockerfile       # Fly.io deployment
│   └── fly.toml         # Fly.io config
├── frontend/            # React app (Vercel)
│   ├── src/             # Components & pages
│   ├── vercel.json      # Vercel config
│   └── package.json
└── README.md
```

## ✨ Features

- 🎤 Speech-to-text (Whisper)
- 🤖 Intent classification (ML)
- 💬 Intelligent responses
- 🔊 Text-to-speech (Edge TTS)
- 🎬 Video generation with lip-sync

## 🛠️ Tech Stack

**Backend:**
- Flask + Gunicorn
- OpenAI Whisper
- Sentence Transformers
- FFmpeg (video processing)

**Frontend:**
- React 19
- Vite
- Tailwind CSS
- React Router

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Full deployment instructions
- [Quick Start](QUICK_START.md) - Deploy in 5 minutes

## 📝 License

MIT License
