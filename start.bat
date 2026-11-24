@echo off
title AI Cartoon Studio Runner
echo ======================================================
echo           Starting AI Cartoon Studio
echo ======================================================
echo.

cd /d "%~dp0"

set "PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

echo [1/2] Starting Backend Server (FastAPI on http://127.0.0.1:8000)...
start "AI Cartoon Studio - Backend" cmd /k "cd /d "%~dp0backend" && "%PYTHON_EXE%" run.py"

echo.
echo [2/2] Starting Frontend App (Vite on http://127.0.0.1:5173)...
start "AI Cartoon Studio - Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ======================================================
echo Both servers are starting in separate windows!
echo Web App UI: http://127.0.0.1:5173
echo API Docs:   http://127.0.0.1:8000/docs
echo ======================================================
pause
