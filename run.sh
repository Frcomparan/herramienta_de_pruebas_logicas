#!/bin/bash

echo "====================================="
echo "Herramienta de Pruebas Lógicas"
echo "====================================="
echo

# Check if .env file exists
if [ ! -f .env ]; then
    echo "[ERROR] Archivo .env no encontrado"
    echo "Por favor, copia .env.template a .env y configura tu GEMINI_API_KEY"
    echo
    exit 1
fi

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker no está instalado o no está ejecutándose"
    echo "Por favor, instala Docker"
    echo
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "[ERROR] Docker Compose no está instalado"
    echo "Por favor, instala Docker Compose"
    echo
    exit 1
fi

echo "[INFO] Construyendo y ejecutando la aplicación con Docker..."
echo

# Build and run with docker-compose
docker-compose up --build

echo
echo "[INFO] La aplicación se ha detenido"