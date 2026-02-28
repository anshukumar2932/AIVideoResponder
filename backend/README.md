# AIVideoResponder Backend

Flask backend for the AI Video Responder application.

## Features

- Speech-to-text processing
- Intent prediction
- Response generation
- Text-to-speech conversion
- Video generation with visemes

## Deployment on Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the root directory to `backend`
4. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3.9.16

## Environment Variables

- `PORT`: Automatically set by Render (default: 5000)

## API Endpoints

- `GET /`: Health check
- `POST /support`: Process audio and generate response
- `GET /video`: Serve generated video

## Local Development

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The server will run on `http://localhost:5000`