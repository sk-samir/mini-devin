@echo off
REM Start Mini Devin Backend Server

echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

echo.
echo Starting FastAPI Backend Server...
echo Backend will run at http://127.0.0.1:8000
echo API docs at http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop.
echo.

python run_backend.py
pause
