#!/usr/bin/env python
"""
Main entry point for running the Streamlit frontend.
Usage: python run_frontend.py
Or: streamlit run ui/streamlit_app.py
"""

import subprocess
import sys
import logging
import logging_config

if __name__ == "__main__":
    # Initialize logging for the launcher
    logging_config.init_logging()

    logger = logging_config.get_logger('main')
    logger.info("🚀 Starting Mini Devin Frontend...")

    print("🚀 Starting Mini Devin Frontend...")
    print("Frontend will run at http://localhost:8501")
    print("Logs available in logs/ directory")
    print("Press Ctrl+C to stop.\n")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py"],
            cwd="."
        )
        logger.info("Frontend stopped normally")
        print("\n✅ Frontend stopped.")
    except KeyboardInterrupt:
        logger.info("Frontend stopped by user")
        print("\n✅ Frontend stopped.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Frontend failed: {str(e)}", exc_info=True)
        print(f"\n❌ Frontend failed: {str(e)}")
        sys.exit(1)
