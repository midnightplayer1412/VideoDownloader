@echo off
echo Setting up Virtual Environment...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python first.
    pause
    exit /b
)

:: Create and activate virtual environment
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Activating venv...

:: Install required packages if not already installed
echo Installing required packages...
pip install -r requirements.txt

:: Run the application
python main.py

:: pause