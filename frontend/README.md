# AIVideoResponder Frontend

React frontend for the AI Video Responder application.

## Features

- Audio recording interface
- Real-time communication with backend
- Video playback of AI responses
- Modern UI with Tailwind CSS

## Deployment on Render

1. Connect your GitHub repository to Render
2. Create a new Static Site
3. Set the root directory to `frontend`
4. Use the following settings:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

## Environment Variables

Create a `.env` file in the frontend directory:

```
VITE_API_URL=https://your-backend-url.onrender.com
```

## Local Development

```bash
cd frontend
npm install
npm run dev
```

The application will run on `http://localhost:5173`

## Build for Production

```bash
npm run build
```

## Technologies Used

- React 19
- Vite
- Tailwind CSS
- React Router DOM