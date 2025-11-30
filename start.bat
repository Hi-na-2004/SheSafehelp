@echo off
REM SafeCircle - Quick Start Script for Windows

echo.
echo ====================================
echo SafeCircle - Women Safety & Support Platform
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    exit /b 1
)

echo [OK] Python found

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo [WARNING] Please edit .env file with your credentials
)

echo.
echo ====================================
echo [OK] Setup complete!
echo.
echo Starting application...
echo.

REM Start the application
cd backend
python app.py

