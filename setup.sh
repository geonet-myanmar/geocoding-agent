#!/bin/bash
# GeoAI Agent Setup Script for macOS/Linux

set -e

echo ""
echo "========================================"
echo "  GeoAI Agent Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/5] Python detected"
python3 --version

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "[ERROR] npm is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "[2/5] npm detected"
npm --version

# Install GitHub Copilot CLI
echo ""
echo "[3/5] Installing GitHub Copilot CLI..."
npm install -g @github/copilot-cli || {
    echo "[WARNING] Failed to install Copilot CLI globally"
    echo "You may need to run with sudo: sudo npm install -g @github/copilot-cli"
}

# Create virtual environment
echo ""
echo "[4/5] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate and install dependencies
echo ""
echo "[5/5] Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Authenticate with GitHub:"
echo "     copilot auth login"
echo ""
echo "  3. Run the basic agent:"
echo "     python geocoding_agent.py"
echo ""
echo "  4. Or run the extended agent:"
echo "     python geocoding_agent_extended.py"
echo ""
echo "See README.md for more information."
echo ""
