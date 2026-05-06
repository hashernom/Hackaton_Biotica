@echo off
echo Iniciando Biotica Backend + Frontend...

start "Backend FastAPI" cmd /k "cd /d C:\Users\santiafanador\Desktop\Hackaton\Hackaton_Biotica && venv\Scripts\activate && uvicorn backend_api:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

start "Frontend Vue" cmd /k "cd /d C:\Users\santiafanador\Desktop\Hackaton\Hackaton_Biotica\frontend && npm run serve"

echo Servidores iniciando...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8081
