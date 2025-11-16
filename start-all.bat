@echo off
echo ==============================================
echo   OrgLead AI - Starting All Services
echo ==============================================

REM Create logs directory
if not exist logs mkdir logs

REM Start Backend
echo.
echo Starting Spring Boot Backend...
cd backend
start "OrgLead Backend" cmd /k "mvnw.cmd spring-boot:run"
cd ..

REM Wait
timeout /t 10 /nobreak

REM Start Python Service
echo.
echo Starting Python AI Service...

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

start "OrgLead Python" cmd /k "python app.py"

echo.
echo ==============================================
echo Services Started!
echo ==============================================
echo.
echo Access points:
echo   - Backend:  http://localhost:8080
echo   - Python:   http://localhost:8000
echo.
echo Close the terminal windows to stop services
echo ==============================================

pause
