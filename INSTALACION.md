# Guía de Instalación Rápida 🚀

## Para Estudiantes - Instalación Fácil con Docker

### 1. Descargar Docker
- Ir a [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Descargar para Windows/Mac/Linux
- Instalar y reiniciar el computador

### 2. Obtener Clave API de Google Gemini
- Ir a [Google AI Studio](https://aistudio.google.com/app/apikey)
- Crear una cuenta Google si no tienes
- Generar una nueva API Key
- **¡Guardar la clave! La necesitarás en el paso 4**

### 3. Descargar el Proyecto
- Descargar todos los archivos del proyecto
- Extraer en una carpeta (ejemplo: `C:\logic-proofs\`)

### 4. Configurar la API Key
- Copiar el archivo `.env.template` y renombrarlo a `.env`
- Abrir `.env` con el Notepad
- Reemplazar `your_gemini_api_key_here` con tu clave API real
- Guardar el archivo

### 5. Ejecutar la Aplicación
**En Windows:**
- Hacer doble clic en `run.bat`
- Esperar que termine de cargar (puede tomar 2-3 minutos la primera vez)

**En Mac/Linux:**
- Abrir Terminal
- Navegar a la carpeta del proyecto: `cd /ruta/al/proyecto`
- Ejecutar: `chmod +x run.sh && ./run.sh`

### 6. Usar la Aplicación
- Abrir navegador
- Ir a: http://localhost:8000
- ¡Ya puedes analizar argumentos lógicos! 🎉

## Ejemplos para Probar

### Ejemplo 1 (Válido):
- **Premisa 1:** Si llueve entonces la calle se moja
- **Premisa 2:** Llueve  
- **Conclusión:** La calle se moja

### Ejemplo 2 (Inválido):
- **Premisa 1:** Si llueve entonces la calle se moja
- **Premisa 2:** La calle se moja
- **Conclusión:** Llueve

## ¿Problemas?

### Error: "GEMINI_API_KEY required"
- Verificar que el archivo `.env` existe
- Verificar que contiene tu clave API real
- Reiniciar la aplicación

### Error: "Port 8000 already in use"
- Cerrar otras aplicaciones que usen el puerto 8000
- O cambiar el puerto en `docker-compose.yml`

### La aplicación no carga
- Verificar que Docker Desktop está ejecutándose
- Esperar más tiempo (primera vez puede tomar varios minutos)
- Revisar que tienes conexión a internet

## Para Parar la Aplicación
- Presionar `Ctrl+C` en la ventana de comandos
- O cerrar la ventana de comandos

---
**¡Listo para explorar la lógica formal! 🧠✨**