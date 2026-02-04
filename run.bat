@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
TITLE Contract Risk Analysis Bot – Hackathon 2026

REM =====================================================
REM CONFIGURATION
REM =====================================================
SET APP_ENTRY=app\app.py
SET VENV_DIR=venv
SET LOG_DIR=logs
SET PYTHON_MIN_VERSION=3.9

REM =====================================================
REM BANNER
REM =====================================================
echo.
echo =====================================================
echo   ⚖️ Contract Analysis & Risk Assessment Bot
echo   🎯 Career Carnival Hackathon 2026
echo =====================================================
echo.

REM =====================================================
REM MOVE TO PROJECT ROOT
REM =====================================================
cd /d "%~dp0"

REM =====================================================
REM CREATE LOG DIRECTORY
REM =====================================================
IF NOT EXIST %LOG_DIR% (
    mkdir %LOG_DIR%
)

SET LOG_FILE=%LOG_DIR%\run_%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%.log
SET LOG_FILE=%LOG_FILE: =0%

echo 🔹 Log file: %LOG_FILE%
echo Starting application... > "%LOG_FILE%"

REM =====================================================
REM CHECK PYTHON
REM =====================================================
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python not found
    echo Install Python %PYTHON_MIN_VERSION%+ and add to PATH
    pause
    exit /b
)

FOR /F "tokens=2 delims= " %%A IN ('python --version') DO SET PY_VER=%%A
echo ✅ Python version: %PY_VER%

REM =====================================================
REM CREATE VENV IF NOT EXISTS
REM =====================================================
IF NOT EXIST %VENV_DIR%\Scripts\activate.bat (
    echo ⚠️ Virtual environment not found
    echo 🔧 Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM =====================================================
REM ACTIVATE VENV
REM =====================================================
call %VENV_DIR%\Scripts\activate.bat
echo ✅ Virtual environment activated

REM =====================================================
REM INSTALL DEPENDENCIES IF NEEDED
REM =====================================================
pip show streamlit >nul 2>&1
IF ERRORLEVEL 1 (
    echo 📦 Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
) ELSE (
    echo ✅ Dependencies already installed
)

REM =====================================================
REM CHECK TESSERACT OCR
REM =====================================================
tesseract --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Tesseract OCR not found
    echo 👉 Install from:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    pause
    exit /b
) ELSE (
    echo ✅ Tesseract OCR detected
)

REM =====================================================
REM CHECK POPPLER (PDF OCR)
REM =====================================================
pdfinfo -v >nul 2>&1
IF ERRORLEVEL 1 (
    echo ⚠️ Poppler not found
    echo OCR will work for images, not scanned PDFs
) ELSE (
    echo ✅ Poppler detected
)

REM =====================================================
REM SET STREAMLIT OPTIONS
REM =====================================================
SET STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
SET STREAMLIT_SERVER_HEADLESS=true
SET STREAMLIT_SERVER_RUN_ON_SAVE=true

REM =====================================================
REM LAUNCH APPLICATION
REM =====================================================
echo.
echo 🚀 Launching Streamlit Application...
echo 🌐 URL: http://localhost:8501
echo.

start http://localhost:8501

streamlit run %APP_ENTRY% ^
    --server.port 8501 ^
    --server.address localhost ^
    --logger.level info ^
    >> "%LOG_FILE%" 2>&1

REM =====================================================
REM CLEAN EXIT
REM =====================================================
echo.
echo 🛑 Application stopped
echo Logs saved to %LOG_FILE%
pause
ENDLOCAL
