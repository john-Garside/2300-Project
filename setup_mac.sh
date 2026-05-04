#!/bin/bash
# Not Steam - macOS setup script
# Installs all dependencies needed to run the application.

set -e # exit immediately if any command fails

echo "=== Not Steam: macOS setup ==="

# Check for Homebrew, install it if missing
if ! command -v brew &>/dev/null; then
  echo "Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew already installed."
fi

echo "Installing Python..."
brew install python

echo "Installing Tkinter..."
brew install python-tk

echo "Installing SQLite..."
brew install sqlite

echo ""
echo "=== Setup complete ==="
echo "Run the app with: python3 gui.py"
