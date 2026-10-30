@echo off
title CIVISENSE — Smart Urban Waterlogging Prevention & Municipal Intelligence
echo =========================================================================
echo    CIVISENSE — Predict. Prioritize. Prevent.
echo    Smart Urban Waterlogging Prevention and Municipal Response System
echo    Pilot Geography: Chandigarh, India
echo =========================================================================
echo.

cd /d "%~dp0"
set ELECTRON_RUN_AS_NODE=1
set PORT=8000

echo Starting CIVISENSE Prototype Server on http://127.0.0.1:8000 ...
start "" "http://127.0.0.1:8000"
"C:\Users\VICTUS\AppData\Local\Programs\antigravity\Antigravity.exe" server.js

pause
