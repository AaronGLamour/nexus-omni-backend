@echo off
title Nexus Omni - Production Server
cd /d "%~dp0"
echo Starting Nexus Omni Production Server...
start /B python main.py
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:5000"
pause
