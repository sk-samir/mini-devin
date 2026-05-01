#!/usr/bin/env python
"""
Main entry point for running the FastAPI backend server.
Usage: python run_backend.py
"""

import sys
import uvicorn
from api.main import app

if __name__ == "__main__":
    print("🚀 Starting Mini Devin Backend...")
    print("Backend running at http://127.0.0.1:8000")
    print("API documentation available at http://127.0.0.1:8000/docs")
    print("Press Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
