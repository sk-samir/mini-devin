@echo off
REM Quick Model Switcher for Mini Devin
REM Usage: Run this script and select a model

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   Mini Devin - Model Switcher
echo ====================================================
echo.
echo Select a model:
echo.
echo   1) Mistral (7B)      - FAST - 5-15s per query
echo   2) Llama3 (8B)       - ACCURATE - 30-180s per query
echo   3) Neural Chat (7B)  - CHAT OPTIMIZED - 5-15s per query
echo   4) Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    set MINI_DEVIN_MODEL=mistral
    echo.
    echo ✅ Model switched to: MISTRAL (Fast)
    echo Downloading model if needed...
    call ollama pull mistral
    echo.
    echo Starting backend with Mistral...
    call .venv\Scripts\activate.bat
    python run_backend.py
) else if "%choice%"=="2" (
    set MINI_DEVIN_MODEL=llama3
    echo.
    echo ✅ Model switched to: LLAMA3 (Accurate)
    echo Downloading model if needed...
    call ollama pull llama3
    echo.
    echo Starting backend with Llama3...
    call .venv\Scripts\activate.bat
    python run_backend.py
) else if "%choice%"=="3" (
    set MINI_DEVIN_MODEL=neural-chat
    echo.
    echo ✅ Model switched to: NEURAL-CHAT (Optimized for Chat)
    echo Downloading model if needed...
    call ollama pull neural-chat
    echo.
    echo Starting backend with Neural Chat...
    call .venv\Scripts\activate.bat
    python run_backend.py
) else if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    timeout /t 2 /nobreak
    goto start
)

:start
goto end

:end
endlocal
