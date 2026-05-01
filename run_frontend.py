#!/usr/bin/env python
"""
Main entry point for running the Streamlit frontend.
Usage: python run_frontend.py
Or: streamlit run ui/streamlit_app.py
"""

import subprocess
import sys

if __name__ == "__main__":
    print("🚀 Starting Mini Devin Frontend...\n")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"],
            cwd="."
        )
    except KeyboardInterrupt:
        print("\n✅ Frontend stopped.")
        sys.exit(0)
