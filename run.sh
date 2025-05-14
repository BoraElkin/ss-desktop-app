#!/bin/bash
set -e

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Optional: Install dependencies if not already installed
if ! pip show fastapi > /dev/null 2>&1; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi

# Launch the app
./src/ui.py 