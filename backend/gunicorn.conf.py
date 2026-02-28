# Gunicorn configuration for Render deployment
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
backlog = 512

# Worker processes - optimized for Render free tier
workers = 1
worker_class = "sync"
worker_connections = 100
timeout = 300  # Increased for model loading
keepalive = 2

# Memory management
max_requests = 100
max_requests_jitter = 10

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Server mechanics
preload_app = True
daemon = False

# Render-specific optimizations
worker_tmp_dir = "/dev/shm"  # Use shared memory for better performance