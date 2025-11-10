@echo off
title MedGuide Chatbot Starter

echo Stopping old Ollama...
taskkill /F /IM ollama.exe /T >nul 2>&1

echo Starting Ollama server...
start cmd /k "ollama serve"
timeout /t 5 >nul

echo Starting your chatbot...
cd /d "C:\Users\Chara\OneDrive\Desktop\rmp chatbot"
start cmd /k "streamlit run app.py"

echo Done! Open http://localhost:8501 in your browser
pause
