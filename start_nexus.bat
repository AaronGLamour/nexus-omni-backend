@'
@echo off
title Nexus Omni - Production Server
cd /d "C:\Users\LinkIts\Desktop\nexus_omni_backend"
echo Starting Nexus Omni Secure System...
start "" "http://127.0.0.1:5000"
python main.py
pause
'@ | Set-Content -Path "start_nexus.bat" -Encoding ASCII