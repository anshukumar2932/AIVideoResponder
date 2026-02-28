#!/bin/bash

echo "🚀 Starting Backend Server"
echo "=========================="

# Check if we're in the right directory
if [ ! -f "backend/app.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Navigate to backend
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment