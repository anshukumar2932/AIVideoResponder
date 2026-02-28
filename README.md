# AIVideoResponder

An AI-powered customer support system that processes voice input and generates video responses with synchronized visemes.

## Project Structure

```
AIVideoResponder/
├── backend/          # Flask API server
│   ├── src/         # Core Python modules
│   ├── database/    # Database files and schemas
│   ├── dataset/     # Video datasets for visemes
│   ├── app.py       # Main Flask application
│   └── requirements.txt
├── frontend/        # React web application
│   ├── src/         # React components and pages
│   ├── public/      # Static assets
│   └── package.json
└── README.md
```

## Features

- **Speech Recognition**: Convert audio input to text using Whisper
- **Intent Classification**: Predict user intent using machine learning
- **Response Generation**: Generate appropriate responses based on intent
- **Text-to-Speech**: Convert responses to audio using Edge TTS
- **Video Generation**: Create videos with synchronized lip movements (visemes)

## Deployment on Render

### Backend Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set root directory to `backend`
4. Configure build and start commands:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3.9.16

### Frontend Deployment

1. Create a new Static Site on Render
2. Connect your GitHub repository
3. Set root directory to `frontend`
4. Configure build settings:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

### Environment Configuration

Update the frontend environment variables to point to your deployed backend:

```bash
# In frontend/.env
VITE_API_URL=https://your-backend-service.onrender.com
```

## Local Development

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## API Documentation

### Endpoints

- `GET /`: Health check
- `POST /support`: Process audio file and return AI response
- `GET /video`: Serve generated response video

### Request Format

```bash
curl -X POST \
  -F "audio=@recording.wav" \
  https://your-backend-url.onrender.com/support
```

### Response Format

```json
{
  "user_text": "I need help with my account",
  "intent": "account_support",
  "response": "I'd be happy to help you with your account...",
  "video_url": "/video"
}
```

## Technologies Used

### Backend
- Flask (Web framework)
- Whisper (Speech recognition)
- Scikit-learn (Intent classification)
- Edge TTS (Text-to-speech)
- OpenCV (Video processing)

### Frontend
- React 19
- Vite (Build tool)
- Tailwind CSS (Styling)
- React Router (Navigation)

## License

MIT License