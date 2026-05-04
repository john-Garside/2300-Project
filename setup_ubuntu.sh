#!/bin/bash
# Not Steam - Ubuntu/Debian setup script
# Installs all dependencies needed to run the application.

set -e

echo "=== Not Steam: Ubuntu setup ==="

echo "Updating package list..."
sudo apt update

echo "Installing Python..."
sudo apt install -y python3

echo "Installing Tkinter..."
sudo apt install -y python3-tk

echo "Installing SQLite..."
sudo apt install -y sqlite3

echo ""
echo "=== Setup complete ==="
echo "Run the app with: python3 gui.py"
