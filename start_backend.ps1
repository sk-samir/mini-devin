# Start Mini Devin Backend Server (PowerShell)

Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starting FastAPI Backend Server..." -ForegroundColor Green
Write-Host "Backend will run at http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "API docs at http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

python run_backend.py
Read-Host "Press Enter to exit"
