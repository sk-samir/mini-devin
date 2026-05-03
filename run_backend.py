#!/usr/bin/env python
"""
Main entry point for running the FastAPI backend server.
Usage: python run_backend.py
"""

import sys
import uvicorn
import logging_config
from api.main import app

if __name__ == "__main__":
    # Initialize logging
    logging_config.init_logging()

    logger = logging_config.get_logger('main')
    logger.info("🚀 Starting Mini Devin Backend...")

    print("🚀 Starting Mini Devin Backend...")
    print("Backend running at http://127.0.0.1:8000")
    print("API documentation available at http://127.0.0.1:8000/docs")
    print("Logs available in logs/ directory")
    print("Press Ctrl+C to stop the server\n")

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        logger.info("Backend server stopped by user")
        print("\n✅ Backend server stopped.")
    except Exception as e:
        logger.error(f"Backend server failed: {str(e)}", exc_info=True)
        print(f"\n❌ Backend server failed: {str(e)}")
        sys.exit(1)
