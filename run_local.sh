#!/bin/bash

echo "🚀 Starting AIVideoResponder Local Development Setup"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete"
echo ""

# Setup Frontend
echo "🔧 Setting up Frontend..."
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete"
echo ""

# Create start script
cd ..
cat > start_dev.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting AIVideoResponder Development Servers"
echo "==============================================="

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start Backend
echo "🔥 Starting Backend Server (Flask)..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Frontend
echo "🎨 Starting Frontend Server (Vite)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Both servers are running!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID
EOF

chmod +x start_dev.sh

echo "🎉 Setup Complete!"
echo ""
echo "To start the development servers, run:"
echo "  ./start_dev.sh"
echo ""
echo "Or start them manually:"
echo "  Backend:  cd backend && source venv/bin/activate && python app.py"
echo "  Frontend: cd frontend && npm run dev"