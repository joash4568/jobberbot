#!/bin/bash

# setup_kali.sh
# Run this script on your Kali Linux machine to set up the bot.

set -e  # Exit immediately if a command exits with a non-zero status.

echo "🚀 Starting Jobber Bot Setup for Kali Linux..."

# 1. Update System & Install Dependencies
# 'libpango' and 'libffi' are crucial for WeasyPrint (Resume Generator)
echo "📦 Installing system dependencies (requires sudo)..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv chromium-driver libpango-1.0-0 libpangoft2-1.0-0 libffi-dev libjpeg-dev libopenjp2-7-dev python3-yaml

# 2. Set up Python Virtual Environment
echo "🐍 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv --system-site-packages
    echo "   -> Virtual environment created."
else
    echo "   -> Virtual environment already exists."
fi

# 3. Activate & Install Python Requirements
echo "⬇️  Installing Python libraries..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel
# 1. Install PyYAML 6.0.1 (Fixes build error on newer Python)
pip install PyYAML==6.0.1
# 2. Install other dependencies
pip install -r requirements.txt
# 3. Install resumy ignoring dependencies (bypasses the strict PyYAML==6.0 conflict)
pip install resumy --no-deps

# 4. Verify Installation
echo "✅ Verifying installation..."
if python3 -c "import weasyprint" &> /dev/null; then
    echo "   -> WeasyPrint (Resume Engine) is ready!"
else
    echo "   -> ⚠️  Warning: WeasyPrint might have issues. Check logs."
fi

echo "------------------------------------------------"
echo "🎉 Setup Complete!"
echo ""
echo "To run the bot:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo "------------------------------------------------"
