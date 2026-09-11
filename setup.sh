#!/bin/bash
set -e

echo "=== AI Image Generator Backend Setup ==="

python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Setup complete. Run with:"
echo "  source venv/bin/activate && python main.py"
