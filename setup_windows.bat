@echo off
REM Not Steam - Windows setup script
REM Installs all dependencies needed to run the application.

echo === Not Steam: Windows setup ===

echo Installing Python...
winget install -e --id Python.Python.3.12

echo Installing SQLite...
winget install -e --id SQLite.SQLite

echo.
echo === Setup complete ===
echo Tkinter is bundled with the Python installer above; no separate install needed.
echo You may need to restart your terminal for python to be on PATH.
echo Run the app with: python gui.py
pause
