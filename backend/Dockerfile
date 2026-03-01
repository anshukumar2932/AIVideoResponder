# Use Python 3.11 (required for scikit-learn >=1.8)
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies (ffmpeg + audio support)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first (for Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port (Render injects $PORT dynamically)
EXPOSE 8080

# Optional healthcheck (Render also has its own)
HEALTHCHECK CMD curl --fail http://localhost:$PORT/ || exit 1

# Start application using dynamic PORT (IMPORTANT FOR RENDER)
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --access-logfile - --error-logfile -"]