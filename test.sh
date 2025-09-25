#!/bin/bash

echo "====================================="
echo "EJECUTOR DE PRUEBAS - HERRAMIENTA DE PRUEBAS LÓGICAS"
echo "====================================="
echo

# Check if .env file exists
if [ ! -f .env ]; then
    echo "[ERROR] Archivo .env no encontrado"
    echo "Por favor, copia .env.template a .env y configura tu GEMINI_API_KEY"
    echo
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no está instalado o no está en el PATH"
    echo "Por favor, instala Python 3.8 o superior"
    echo
    exit 1
fi

echo "[INFO] Instalando dependencias..."
pip3 install -r requirements.txt

echo
echo "====================================="
echo "OPCIONES DE PRUEBA:"
echo "====================================="
echo "1. Ejecutar pruebas unitarias (pytest)"
echo "2. Ejecutar casos de prueba manuales"
echo "3. Ver resumen de casos de prueba"
echo "4. Ejecutar todas las pruebas"
echo "====================================="

read -p "Selecciona una opción (1-4): " choice

case $choice in
    1)
        echo
        echo "[INFO] Ejecutando pruebas unitarias..."
        python3 -m pytest test_logic.py -v
        ;;
    2)
        echo
        echo "[INFO] Ejecutando casos de prueba manuales..."
        echo "[NOTA] Necesitas tener configurada tu GEMINI_API_KEY"
        python3 run_test_cases.py
        ;;
    3)
        echo
        echo "[INFO] Mostrando resumen de casos de prueba..."
        python3 test_cases.py
        ;;
    4)
        echo
        echo "[INFO] Ejecutando todas las pruebas..."
        echo
        echo "=== PRUEBAS UNITARIAS ==="
        python3 -m pytest test_logic.py -v
        echo
        echo "=== RESUMEN DE CASOS ==="
        python3 test_cases.py
        ;;
    *)
        echo "[ERROR] Opción inválida"
        ;;
esac

echo
echo "[INFO] Pruebas completadas"