@echo off
REM GeoAI Agent Setup Script for Windows

echo.
echo ========================================
echo   GeoAI Agent Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python detected
python --version

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [2/5] npm detected
npm --version

REM Install GitHub Copilot CLI
echo.
echo [3/5] Installing GitHub Copilot CLI...
call npm install -g @github/copilot-cli
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install Copilot CLI globally
    echo You may need to run this script as Administrator
)

REM Create virtual environment
echo.
echo [4/5] Creating Python virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate and install dependencies
echo.
echo [5/5] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Authenticate with GitHub:
echo      copilot auth login
echo.
echo   2. Run the basic agent:
echo      python geocoding_agent.py
echo.
echo   3. Or run the extended agent:
echo      python geocoding_agent_extended.py
echo.
echo See README.md for more information.
echo.
pause
