#!/usr/bin/env python3
"""
Startup script for Render deployment
Handles model loading and initialization
"""
import os
import sys
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if we're running on Render"""
    is_render = os.environ.get('RENDER') == 'true'
    logger.info(f"Running on Render: {is_render}")
    return is_render

def preload_models():
    """Preload models to reduce cold start time"""
    try:
        logger.info("Starting model preloading...")
        
        # Import and initialize models
        from src.predict_intent import predict_intent
        from src.response_generator import generate_response
        
        # Test with a simple prediction to warm up models
        test_text = "hello"
        intent = predict_intent(test_text)
        response = generate_response(intent)
        
        logger.info(f"Models preloaded successfully. Test: '{test_text}' -> '{intent}' -> '{response[:50]}...'")
        return True
        
    except Exception as e:
        logger.error(f"Failed to preload models: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("Starting AIVideoResponder backend...")
    
    # Check environment
    is_render = check_environment()
    
    if is_render:
        logger.info("Render environment detected - optimizing for cloud deployment")
        
        # Preload models
        if preload_models():
            logger.info("Model preloading completed successfully")
        else:
            logger.warning("Model preloading failed - continuing anyway")
    
    # Import and start the Flask app
    from app import app
    
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask app on port {port}")
    
    if is_render:
        # On Render, use gunicorn (this won't be reached, but good for reference)
        logger.info("Use gunicorn for production deployment")
    else:
        # Local development
        app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()