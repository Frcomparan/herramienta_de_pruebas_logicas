@echo off
echo =====================================
echo EJECUTOR DE PRUEBAS - HERRAMIENTA DE PRUEBAS LÓGICAS
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

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior
    echo.
    pause
    exit /b 1
)

echo [INFO] Instalando dependencias...
pip install -r requirements.txt

echo.
echo =====================================
echo OPCIONES DE PRUEBA:
echo =====================================
echo 1. Ejecutar pruebas unitarias (pytest)
echo 2. Ejecutar casos de prueba manuales
echo 3. Ver resumen de casos de prueba
echo 4. Ejecutar todas las pruebas
echo =====================================

set /p choice="Selecciona una opción (1-4): "

if "%choice%"=="1" (
    echo.
    echo [INFO] Ejecutando pruebas unitarias...
    python -m pytest test_logic.py -v
) else if "%choice%"=="2" (
    echo.
    echo [INFO] Ejecutando casos de prueba manuales...
    echo [NOTA] Necesitas tener configurada tu GEMINI_API_KEY
    python run_test_cases.py
) else if "%choice%"=="3" (
    echo.
    echo [INFO] Mostrando resumen de casos de prueba...
    python test_cases.py
) else if "%choice%"=="4" (
    echo.
    echo [INFO] Ejecutando todas las pruebas...
    echo.
    echo === PRUEBAS UNITARIAS ===
    python -m pytest test_logic.py -v
    echo.
    echo === RESUMEN DE CASOS ===
    python test_cases.py
) else (
    echo [ERROR] Opción inválida
)

echo.
echo [INFO] Pruebas completadas
pause