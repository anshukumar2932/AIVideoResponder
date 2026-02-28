# Running AIVideoResponder on Localhost

Follow these steps to run the backend and frontend in separate terminals using virtual environments.

## Prerequisites

Make sure you have:
- Python 3.8+ installed
- Node.js 16+ installed
- npm installed

## Terminal 1: Backend Setup

### Step 1: Navigate to backend directory
```bash
cd backend
```

### Step 2: Create and activate virtual environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# On Windows use:
# venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run the Flask backend
```bash
python app.py
```

The backend will start on `http://localhost:5000`

You should see:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000
```

## Terminal 2: Frontend Setup

### Step 1: Navigate to frontend directory
```bash
cd frontend
```

### Step 2: Install Node.js dependencies
```bash
npm install
```

### Step 3: Run the React development server
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

You should see:
```
  VITE v7.3.1  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Testing the Application

1. Open your browser and go to `http://localhost:5173`
2. The frontend should load and be able to communicate with the backend
3. Test the audio recording and processing functionality

## Troubleshooting

### Backend Issues

**Import Errors:**
If you get import errors, make sure all files are in the correct location:
- `stt.py`, `tts.py`, `generate_video.py` should be in the `backend/` directory
- `src/` folder with Python modules should be in `backend/src/`

**Missing Dependencies:**
If some packages fail to install due to disk space:
```bash
# Install core dependencies first
pip install flask flask-cors
pip install numpy pandas scikit-learn

# Install ML dependencies separately
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers
```

**Port Already in Use:**
If port 5000 is busy, modify `backend/app.py`:
```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Change to 5001
    app.run(host="0.0.0.0", port=port)
```

### Frontend Issues

**Node.js Version:**
Make sure you're using Node.js 16 or higher:
```bash
node --version
npm --version
```

**Port Already in Use:**
If port 5173 is busy, Vite will automatically try the next available port.

**API Connection Issues:**
Update the API URL in `frontend/.env`:
```
VITE_API_URL=http://localhost:5000
```

If you changed the backend port, update accordingly.

## Development Workflow

### Making Changes

**Backend Changes:**
1. Make your changes to Python files
2. The Flask server will auto-reload (if debug mode is enabled)
3. If it doesn't reload, stop the server (Ctrl+C) and restart with `python app.py`

**Frontend Changes:**
1. Make your changes to React components
2. Vite will automatically hot-reload the browser
3. Changes should appear immediately

### Stopping the Servers

To stop either server:
1. Go to the respective terminal
2. Press `Ctrl+C`
3. Deactivate the Python virtual environment: `deactivate`

## Quick Start Commands

Save these commands for easy reference:

**Backend Terminal:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Frontend Terminal:**
```bash
cd frontend
npm run dev
```

## Environment Variables

### Backend
No additional environment variables needed for local development.

### Frontend
Create `frontend/.env`:
```
VITE_API_URL=http://localhost:5000
```

## File Structure Check

Make sure your project structure looks like this:
```
AIVideoResponder/
├── backend/
│   ├── venv/                 # Virtual environment
│   ├── src/                  # Python modules
│   ├── database/             # Database files
│   ├── dataset/              # Video datasets
│   ├── app.py               # Main Flask app
│   ├── requirements.txt     # Python dependencies
│   ├── stt.py              # Speech to text
│   ├── tts.py              # Text to speech
│   └── generate_video.py   # Video generation
├── frontend/
│   ├── node_modules/        # Node dependencies
│   ├── src/                 # React components
│   ├── public/              # Static files
│   ├── package.json         # Node dependencies
│   └── .env                 # Environment variables
└── README.md
```