@echo off
echo =====================================
echo Herramienta de Pruebas Lógicas
echo =====================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [ERROR] Archivo .env no encontrado
    echo Por favor, copia .env.template a .env y configura tu GEMINI_API_KEY
    echo.
    pause
    exit /b 1
)

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no está instalado o no está ejecutándose
    echo Por favor, instala Docker Desktop para Windows
    echo.
    pause
    exit /b 1
)

echo [INFO] Construyendo y ejecutando la aplicación con Docker...
echo.

REM Build and run with docker-compose
docker-compose up --build

echo.
echo [INFO] La aplicación se ha detenido
pause