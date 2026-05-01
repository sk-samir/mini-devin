@echo off
REM Start Mini Devin Frontend (Streamlit)

echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

echo.
echo Starting Streamlit Frontend...
echo Frontend will run at http://localhost:8501
echo.
echo Press Ctrl+C to stop.
echo.

python run_frontend.py
pause
