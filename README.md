# Herramienta de Pruebas Lógicas 🧠

Una aplicación web monolítica y contenerizada desarrollada con FastAPI que permite a los usuarios introducir argumentos en lenguaje natural, analizarlos y generar pruebas deductivas paso a paso utilizando reglas de inferencia formales.

## 🎯 Características Principales

- **Interfaz Web Intuitiva**: Formulario HTML con campos dinámicos para premisas y conclusión
- **Procesamiento de Lenguaje Natural**: Conversión automática de texto a lógica simbólica
- **Validación de Argumentos**: Determinación de validez lógica usando reglas de inferencia estándar
- **Pruebas Deductivas**: Generación paso a paso de derivaciones lógicas para argumentos válidos
- **Contraejemplos**: Generación automática de contraejemplos para argumentos inválidos
- **Contenerización**: Aplicación completamente dockerizada para fácil despliegue

## 🔧 Stack Tecnológico

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5 + Tailwind CSS + Jinja2
- **IA**: Google Gemini API para procesamiento de lenguaje natural
- **Contenerización**: Docker + Docker Compose

## 📋 Reglas de Inferencia Soportadas

- **Modus Ponens**: P → Q, P ⊢ Q
- **Modus Tollens**: P → Q, ¬Q ⊢ ¬P
- **Silogismo Hipotético**: P → Q, Q → R ⊢ P → R
- **Silogismo Disyuntivo**: P ∨ Q, ¬P ⊢ Q
- **Conjunción**: P, Q ⊢ P ∧ Q
- **Simplificación**: P ∧ Q ⊢ P (o Q)
- **Adición**: P ⊢ P ∨ Q
- **Resolución**: (P ∨ Q), (¬P ∨ R) ⊢ (Q ∨ R)

## 🚀 Instalación y Configuración

### Prerequisitos

- Docker y Docker Compose instalados
- Clave API de Google Gemini ([obtener aquí](https://aistudio.google.com/app/apikey))

### Configuración Rápida con Docker

1. **Clonar el repositorio** (o descargar los archivos):
```bash
git clone <repository-url>
cd proyecto-u1
```

2. **Configurar variables de entorno**:
```bash
# Copiar el template de environment
cp .env.template .env

# Editar .env y agregar tu API key de Gemini
# GEMINI_API_KEY=tu_clave_api_aquí
```

3. **Construir y ejecutar con Docker Compose**:
```bash
docker-compose up --build
```

4. **Acceder a la aplicación**:
   - Abrir navegador en: http://localhost:8000
   - La aplicación estará lista para usar

### Instalación Manual (Desarrollo)

1. **Crear entorno virtual**:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:
```bash
cp .env.template .env
# Editar .env con tu API key
```

4. **Ejecutar la aplicación**:
```bash
cd app
python main.py
# o
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Guía de Uso

### Ejemplo 1: Argumento Válido (Modus Ponens)

**Entrada:**
- Premisa 1: "Si llueve entonces la calle se moja"
- Premisa 2: "Llueve"
- Conclusión: "La calle se moja"

**Salida:**
- ✅ **Argumento Válido**
- **Derivación paso a paso:**
  1. Si llueve entonces la calle se moja (P → Q) - Premisa
  2. Llueve (P) - Premisa
  3. La calle se moja (Q) - Modus Ponens (1,2)

### Ejemplo 2: Argumento Inválido

**Entrada:**
- Premisa 1: "Si llueve entonces la calle se moja"
- Premisa 2: "La calle se moja"
- Conclusión: "Llueve"

**Salida:**
- ❌ **Argumento Inválido**
- **Contraejemplo:** P=Falso, Q=Verdadero
  - Premisas verdaderas, conclusión falsa

## 🐳 Comandos Docker Útiles

```bash
# Construir la imagen
docker-compose build

# Ejecutar en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar la aplicación
docker-compose down

# Reiniciar la aplicación
docker-compose restart

# Ver estado de contenedores
docker-compose ps
```

## 🏗️ Estructura del Proyecto

```
proyecto-u1/
├── app/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models.py            # Modelos de datos Pydantic
│   ├── logic_processor.py   # Procesador lógico principal
│   └── templates/
│       ├── index.html       # Página principal
│       └── results.html     # Página de resultados
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación Docker
├── .env.template          # Template de variables de entorno
└── README.md              # Esta documentación
```

## 🔧 API Endpoints

- `GET /` - Página principal con formulario
- `POST /validate` - Validación de argumentos
- `GET /health` - Health check para monitoreo

## 🧪 Testing y Casos de Prueba

### Casos de Prueba Incluidos

La aplicación incluye **24 casos de prueba comprehensivos**:
- **12 casos válidos** (argumentos lógicamente correctos)
- **12 casos inválidos** (falacias comunes)

#### Casos Válidos ✅
- Modus Ponens, Modus Tollens
- Silogismo Hipotético, Silogismo Disyuntivo  
- Conjunción, Simplificación, Adición
- Dilema Constructivo, Resolución
- Casos complejos con 3-4 premisas

#### Casos Inválidos ❌
- Afirmación del Consecuente
- Negación del Antecedente
- Non Sequitur, Falso Dilema
- Generalización Apresurada
- Falacias de Composición, Hombre de Paja
- Post Hoc Ergo Propter Hoc

### Ejecutar Pruebas

#### Opción 1: Script Automatizado
```bash
# Windows
test.bat

# Linux/Mac  
chmod +x test.sh && ./test.sh
```

#### Opción 2: Comandos Individuales
```bash
# Pruebas unitarias
python -m pytest test_logic.py -v

# Ver casos de prueba disponibles
python test_cases.py

# Ejecutar casos de prueba interactivos (requiere API)
python run_test_cases.py
```

### Pruebas Manuales Web

Para probar la interfaz web:

1. **Acceder** en http://localhost:8000
2. **Usar los casos de ejemplo** incluidos en `test_cases.py`
3. **Verificar resultados** contra las expectativas documentadas

#### Ejemplo de Caso Válido:
- **Premisa 1:** Si la alarma suena, entonces hay un incendio
- **Premisa 2:** La alarma está sonando
- **Conclusión:** Hay un incendio
- **Resultado Esperado:** ✅ Válido (Modus Ponens)

#### Ejemplo de Caso Inválido:
- **Premisa 1:** Si un animal es un perro, entonces es un mamífero  
- **Premisa 2:** Mi mascota es un mamífero
- **Conclusión:** Mi mascota es un perro
- **Resultado Esperado:** ❌ Inválido (Afirmación del Consecuente)

## 🚨 Solución de Problemas

### Error: API Key no configurada
```
ValueError: GEMINI_API_KEY environment variable is required
```
**Solución:** Asegúrate de que el archivo `.env` contiene tu clave API válida de Gemini.

### Error: Puerto ocupado
```
Error: Port 8000 is already in use
```
**Solución:** Cambiar el puerto en `docker-compose.yml` o parar otros servicios en el puerto 8000.

### Error de conexión API
**Solución:** Verificar que la clave API de Gemini sea válida y que haya conectividad a internet.

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte del curso de Matemáticas Discretas. Para mejoras o sugerencias:

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto es para uso educativo en el contexto del curso de Matemáticas Discretas.

## 👨‍💻 Autor

Desarrollado para el proyecto de la Unidad 1 - Matemáticas Discretas, Maestría Semestre 1.

---

**¡Explora el fascinante mundo de la lógica formal con esta herramienta interactiva! 🎓**