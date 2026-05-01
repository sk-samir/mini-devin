# Start Mini Devin Frontend (Streamlit) - PowerShell

Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\.venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starting Streamlit Frontend..." -ForegroundColor Green
Write-Host "Frontend will run at http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

python run_frontend.py
Read-Host "Press Enter to exit"
