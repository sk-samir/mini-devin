# Quick Model Switcher for Mini Devin (PowerShell)
# Usage: .\switch_model.ps1

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   Mini Devin - Model Switcher" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Select a model:" -ForegroundColor Green
Write-Host ""
Write-Host "  1) Mistral (7B)      - FAST - 5-15s per query" -ForegroundColor Yellow
Write-Host "  2) Llama3 (8B)       - ACCURATE - 30-180s per query" -ForegroundColor Blue
Write-Host "  3) Neural Chat (7B)  - CHAT OPTIMIZED - 5-15s per query" -ForegroundColor Magenta
Write-Host "  4) Check Current Model" -ForegroundColor White
Write-Host "  5) Exit" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "✅ Model switched to: MISTRAL (Fast)" -ForegroundColor Green
        Write-Host "Downloading model if needed..." -ForegroundColor Gray
        
        $env:MINI_DEVIN_MODEL = "mistral"
        ollama pull mistral
        
        Write-Host ""
        Write-Host "Starting backend with Mistral..." -ForegroundColor Green
        .\.venv\Scripts\Activate.ps1
        python run_backend.py
    }
    "2" {
        Write-Host ""
        Write-Host "✅ Model switched to: LLAMA3 (Accurate)" -ForegroundColor Blue
        Write-Host "Downloading model if needed..." -ForegroundColor Gray
        
        $env:MINI_DEVIN_MODEL = "llama3"
        ollama pull llama3
        
        Write-Host ""
        Write-Host "Starting backend with Llama3..." -ForegroundColor Blue
        .\.venv\Scripts\Activate.ps1
        python run_backend.py
    }
    "3" {
        Write-Host ""
        Write-Host "✅ Model switched to: NEURAL-CHAT (Chat Optimized)" -ForegroundColor Magenta
        Write-Host "Downloading model if needed..." -ForegroundColor Gray
        
        $env:MINI_DEVIN_MODEL = "neural-chat"
        ollama pull neural-chat
        
        Write-Host ""
        Write-Host "Starting backend with Neural Chat..." -ForegroundColor Magenta
        .\.venv\Scripts\Activate.ps1
        python run_backend.py
    }
    "4" {
        Write-Host ""
        Write-Host "Checking current model configuration..." -ForegroundColor Gray
        .\.venv\Scripts\Activate.ps1
        python config.py
        Write-Host ""
        Read-Host "Press Enter to continue"
    }
    "5" {
        Write-Host "Goodbye!" -ForegroundColor Green
        exit
    }
    default {
        Write-Host "❌ Invalid choice. Please try again." -ForegroundColor Red
        Start-Sleep -Seconds 2
        & $PSCommandPath
    }
}
