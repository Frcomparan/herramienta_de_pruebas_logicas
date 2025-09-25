# Herramienta de Pruebas Lógicas 🧠

Una aplicación web monolítica y contenerizada desarrollada con FastAPI que permite a los usuarios introducir argumentos en lenguaje natural, analizarlos y generar pruebas deductivas paso a paso utilizando reglas de inferencia formales. Esta herramienta está diseñada específicamente para estudiantes de **Matemáticas Discretas** que deseen comprender y practicar con la lógica proposicional de manera interactiva.

## 🎯 Características Principales

- **Interfaz Web Intuitiva**: Formulario HTML con campos dinámicos para premisas y conclusión, diseñado pensando en la experiencia del usuario estudiante
- **Procesamiento de Lenguaje Natural**: Conversión automática de texto en español a lógica simbólica estándar
- **Validación de Argumentos**: Determinación de validez lógica usando reglas de inferencia formales reconocidas académicamente
- **Pruebas Deductivas**: Generación paso a paso de derivaciones lógicas para argumentos válidos, mostrando cada aplicación de reglas
- **Contraejemplos**: Generación automática de contraejemplos con asignaciones de verdad para argumentos inválidos
- **Contenerización**: Aplicación completamente dockerizada para garantizar portabilidad y facilidad de despliegue en cualquier entorno

## 🔧 Stack Tecnológico y Justificación

### **Backend: FastAPI (Python)**
**¿Por qué FastAPI?**
- **Alto Rendimiento**: FastAPI es uno de los frameworks web más rápidos para Python, comparable a NodeJS y Go
- **Tipado Automático**: Integración nativa con Pydantic para validación automática de datos y documentación API
- **Asíncrono por Defecto**: Soporte nativo para programación asíncrona, ideal para integraciones con APIs externas como Gemini
- **Documentación Automática**: Genera documentación interactiva automáticamente (Swagger/OpenAPI)
- **Curva de Aprendizaje**: Sintaxis intuitiva y clara, perfecta para proyectos académicos

### **Frontend: HTML5 + Tailwind CSS + Jinja2**
**¿Por qué esta combinación?**
- **Tailwind CSS**: Framework de utilidades CSS que permite desarrollo rápido sin escribir CSS personalizado
  - Diseño responsivo automático
  - Consistencia visual garantizada
  - Fácil mantenimiento y modificación
- **Jinja2**: Motor de plantillas robusto y familiar para desarrolladores Python
  - Sintaxis clara y legible
  - Herencia de plantillas para código reutilizable
  - Integración perfecta con FastAPI
- **HTML5 Semántico**: Estructura clara y accesible, importante para aplicaciones educativas

### **Inteligencia Artificial: Google Gemini API**
**¿Por qué Gemini?**
- **Procesamiento de Lenguaje Natural Avanzado**: Capacidad superior para entender el español coloquial y convertirlo a lógica formal
- **Razonamiento Lógico**: Entrenado específicamente para tareas de razonamiento y matemáticas
- **API Gratuita**: Tier gratuito generoso, ideal para proyectos estudiantiles
- **Respuestas Estructuradas**: Capacidad para generar respuestas en formato JSON estructurado
- **Documentación Excelente**: APIs bien documentadas y fáciles de implementar

### **Contenerización: Docker + Docker Compose**
**¿Por qué Docker?**
- **Portabilidad**: La aplicación funciona idénticamente en cualquier sistema operativo
- **Aislamiento**: Evita conflictos de dependencias con otros proyectos
- **Reproducibilidad**: Garantiza que todos los estudiantes tengan el mismo entorno
- **Facilidad de Despliegue**: Un solo comando para ejecutar toda la aplicación
- **Escalabilidad**: Fácil de escalar o modificar la arquitectura en el futuro

### **Testing: pytest + pytest-asyncio**
**¿Por qué este framework de testing?**
- **pytest**: El framework de testing más popular y poderoso para Python
  - Sintaxis simple y clara
  - Fixtures avanzadas para configuración de pruebas
  - Plugins extensivos (como pytest-asyncio)
- **pytest-asyncio**: Soporte especializado para testing de código asíncrono
  - Esencial para probar las integraciones con APIs externas
  - Manejo correcto de event loops en pruebas

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

## 🏗️ Estructura del Proyecto y Explicación de Archivos

```
proyecto-u1/
├── app/                          # 📁 Código fuente principal de la aplicación
│   ├── main.py                   # 🚀 Aplicación FastAPI principal - Punto de entrada y rutas HTTP
│   ├── models.py                 # 📊 Modelos de datos Pydantic - Estructuras de datos y validación
│   ├── logic_processor.py        # 🧠 Procesador lógico principal - Lógica de IA y validación
│   └── templates/                # 🎨 Plantillas HTML con Jinja2
│       ├── index.html           # 🏠 Página principal - Formulario de entrada de argumentos
│       └── results.html         # 📋 Página de resultados - Visualización de pruebas y contraejemplos
├── 
├── 🧪 ARCHIVOS DE TESTING Y CALIDAD
├── test_cases.py                 # 📚 Base de datos de casos de prueba (24 casos válidos/inválidos)
├── test_logic.py                 # 🔬 Suite de pruebas unitarias comprehensivas
├── run_test_cases.py             # 🎮 Ejecutor interactivo para testing manual con API real
├── 
├── 🐳 CONTAINERIZACIÓN Y DESPLIEGUE  
├── Dockerfile                    # 🐋 Configuración de imagen Docker - Definición del contenedor
├── docker-compose.yml            # 🎼 Orquestación Docker - Configuración de servicios
├── 
├── 📋 CONFIGURACIÓN Y DEPENDENCIAS
├── requirements.txt              # 📦 Dependencias Python con versiones específicas
├── .env.template                 # 🔑 Plantilla de variables de entorno (API keys, configuración)
├── .env.example                  # 💡 Ejemplo de configuración para referencia
├── .gitignore                    # 🚫 Archivos excluidos del control de versiones
├── 
├── 📖 DOCUMENTACIÓN Y GUÍAS
├── README.md                     # 📚 Esta documentación completa
├── INSTALACION.md                # 🚀 Guía de instalación rápida para estudiantes
├── 
└── 🔧 SCRIPTS DE AUTOMATIZACIÓN
    ├── run.bat / run.sh          # ▶️ Scripts para ejecutar la aplicación (Windows/Linux)
    └── test.bat / test.sh        # 🧪 Scripts para ejecutar todas las pruebas
```

### **📝 Explicación Detallada de Archivos Clave:**

#### **🧪 Archivos de Testing (Fundamentación Académica)**

**`test_logic.py` - Pruebas Unitarias**
Las **pruebas unitarias** son un fundamento esencial en el desarrollo de software que consiste en verificar que cada componente individual de la aplicación funcione correctamente de forma aislada. En el contexto de esta herramienta lógica:

- **Propósito Académico**: Garantizan que la lógica matemática implementada sea correcta y confiable
- **Verificación de Modelos**: Validan que las estructuras de datos (ArgumentRequest, ValidationResult, ProofStep) se comporten según especificaciones
- **Testing de Algoritmos**: Verifican que las funciones de conversión simbólica y validación lógica produzcan resultados esperados
- **Regresión**: Aseguran que cambios futuros no rompan funcionalidades existentes
- **Confianza**: Proporcionan seguridad de que la herramienta es académicamente sólida

**`test_cases.py` - Casos de Prueba Estructurados**
Contiene 24 casos de prueba cuidadosamente diseñados que cubren:
- **Argumentos Válidos**: Todos los tipos de reglas de inferencia estándar (Modus Ponens, Modus Tollens, etc.)
- **Argumentos Inválidos**: Falacias lógicas comunes que los estudiantes deben aprender a identificar
- **Variedad de Complejidad**: Desde casos simples (2 premisas) hasta complejos (4 premisas)

**`run_test_cases.py` - Testing Interactivo**
Herramienta para probar la aplicación con casos reales usando la API de Gemini, permitiendo:
- Ejecutar casos individuales o completos
- Verificar que la IA produce resultados académicamente correctos
- Generar reportes de precisión y confiabilidad

## 🔧 API Endpoints

- `GET /` - Página principal con formulario
- `POST /validate` - Validación de argumentos
- `GET /health` - Health check para monitoreo

## 🧪 Sistema de Testing y Aseguramiento de Calidad

### **¿Qué son las Pruebas Unitarias y por qué son Importantes?**

Las **pruebas unitarias** son un componente fundamental de la ingeniería de software que consiste en verificar que cada "unidad" o componente individual de código funcione correctamente de manera aislada. En el contexto académico y de esta herramienta:

#### **Importancia Académica:**
- **Verificación Matemática**: Garantizan que los algoritmos lógicos implementados sean matemáticamente correctos
- **Confiabilidad**: Aseguran que la herramienta produzca resultados consistentes y confiables para el aprendizaje
- **Documentación Viviente**: Las pruebas sirven como ejemplos de cómo debe comportarse cada componente
- **Prevención de Errores**: Detectan problemas antes de que lleguen a los estudiantes usuarios

#### **En esta Aplicación Específicamente:**
- **Validación de Lógica Proposicional**: Verifican que las reglas de inferencia se apliquen correctamente
- **Testing de Casos Edge**: Prueban situaciones límite y casos especiales
- **Verificación de Falacias**: Aseguran que las falacias lógicas se detecten apropiadamente

### **Casos de Prueba Incluidos - Cobertura Académica Completa**

La aplicación incluye **24 casos de prueba meticulosamente diseñados** basados en literatura académica de lógica formal:

#### **✅ 12 Casos Válidos (Argumentos Lógicamente Correctos)**
Estos casos están fundamentados en las **reglas de inferencia clásicas** de la lógica proposicional:

- **Modus Ponens**: La regla más fundamental (P → Q, P ⊢ Q)
- **Modus Tollens**: Inferencia por contraposición (P → Q, ¬Q ⊢ ¬P)
- **Silogismo Hipotético**: Transitividad de implicaciones (P → Q, Q → R ⊢ P → R)
- **Silogismo Disyuntivo**: Eliminación por disyunción (P ∨ Q, ¬P ⊢ Q)
- **Conjunción y Simplificación**: Operaciones con conjunciones
- **Dilema Constructivo**: Casos complejos con múltiples implicaciones
- **Resolución**: Técnica avanzada de demostración automática

#### **❌ 12 Casos Inválidos (Falacias Lógicas Comunes)**
Basados en el catálogo académico de **falacias lógicas formales e informales**:

- **Afirmación del Consecuente**: Error común al invertir implicaciones
- **Negación del Antecedente**: Malinterpretación de la implicación
- **Non Sequitur**: Conclusiones que no se siguen de las premisas
- **Falso Dilema**: Presentar falsas dicotomías
- **Generalización Apresurada**: Inducción inválida
- **Post Hoc Ergo Propter Hoc**: Confundir correlación con causación
- **Hombre de Paja**: Distorsión de argumentos
- **Petición de Principio**: Razonamiento circular

#### **📊 Distribución y Complejidad:**
- **Casos Simples**: 2 premisas (nivel introductorio)
- **Casos Intermedios**: 3 premisas (nivel intermedio)
- **Casos Avanzados**: 4 premisas (nivel avanzado)
- **Cobertura Curricular**: Alineados con programas de Matemáticas Discretas estándar

### **🔬 Ejecutar el Sistema de Testing**

#### **Opción 1: Scripts Automatizados (Recomendado para Estudiantes)**
```bash
# Windows - Ejecutar desde PowerShell
test.bat

# Linux/Mac - Ejecutar desde Terminal
chmod +x test.sh && ./test.sh
```

**¿Qué hacen estos scripts?**
- Verifican que Python esté instalado
- Instalan automáticamente las dependencias de testing
- Ofrecen menú interactivo con múltiples opciones de testing
- Ejecutan pruebas unitarias y muestran resultados detallados

#### **Opción 2: Comandos Individuales (Para Desarrolladores Avanzados)**

**Pruebas Unitarias Básicas:**
```bash
# Ejecutar todas las pruebas unitarias con reporte detallado
python -m pytest test_logic.py -v

# Ejecutar con cobertura de código
python -m pytest test_logic.py --cov=app --cov-report=html
```

**Exploración de Casos de Prueba:**
```bash
# Ver resumen completo de los 24 casos disponibles
python test_cases.py

# Salida: Listado organizado de casos válidos/inválidos con descripciones
```

**Testing Interactivo con IA Real:**
```bash
# Ejecutar casos contra la API real de Gemini (requiere GEMINI_API_KEY)
python run_test_cases.py

# Funcionalidades:
# - Menú interactivo para seleccionar casos específicos
# - Ejecución de suites completas (válidos/inválidos/todos)
# - Generación de reportes de precisión
# - Guardado de resultados en JSON
```

#### **Opción 3: Testing Integrado en IDE**
Si usas **Visual Studio Code**:
- Instala la extensión "Python Test Explorer"
- Los tests aparecerán automáticamente en el panel de testing
- Ejecución individual con un clic
- Debugging integrado para casos específicos

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

## 🎓 Valor Educativo y Aplicación Académica

### **¿Por qué esta Arquitectura Tecnológica para Matemáticas Discretas?**

Esta herramienta fue diseñada específicamente con principios pedagógicos en mente:

#### **� Fundamentación Pedagógica:**
- **Aprendizaje Activo**: Los estudiantes interactúan directamente con conceptos abstractos de lógica
- **Feedback Inmediato**: Respuestas instantáneas que refuerzan el aprendizaje
- **Visualización**: Representación clara de conceptos simbólicos complejos
- **Práctica Guiada**: Casos de prueba estructurados que van de lo simple a lo complejo

#### **🔧 Decisiones Técnicas Educativas:**
- **Interfaz en Español**: Reduce barreras idiomáticas para estudiantes hispanohablantes
- **Containerización**: Elimina problemas técnicos de instalación, permitiendo focus en el contenido
- **API Moderna**: Introduce a estudiantes a tecnologías actuales de la industria
- **Testing Riguroso**: Enseña la importancia de la verificación en matemáticas computacionales

### **💡 Beneficios para el Aprendizaje:**

1. **Comprensión Conceptual**: Transición clara entre lenguaje natural y lógica formal
2. **Identificación de Errores**: Reconocimiento automático de falacias comunes
3. **Práctica Sistemática**: 24 casos cuidadosamente seleccionados para cobertura curricular
4. **Verificación Independiente**: Los estudiantes pueden validar su razonamiento manual

### **🚀 Extensibilidad Futura:**

La arquitectura modular permite fáciles extensiones:
- Agregar nuevos tipos de lógica (predicados, modal, temporal)
- Integrar con sistemas de gestión de aprendizaje (LMS)
- Añadir métricas de progreso estudiantil
- Implementar sistemas de hints y ayuda contextual

## 👨‍💻 Autoría y Contexto Académico

**Proyecto desarrollado para:**
- **Curso**: Matemáticas Discretas - Unidad 1 (Lógica Proposicional)
- **Nivel**: Maestría - Semestre 1
- **Objetivo**: Crear una herramienta práctica para el aprendizaje de reglas de inferencia y detección de falacias
- **Enfoque**: Combinar rigor académico con usabilidad práctica

**Tecnologías seleccionadas por:**
- Relevancia en la industria actual del software
- Facilidad de aprendizaje para estudiantes
- Robustez y escalabilidad para uso educativo
- Compatibilidad multiplataforma

---

## 🌟 Reflexión Final

Esta herramienta representa la **convergencia entre matemáticas tradicionales y tecnología moderna**, demostrando cómo conceptos fundamentales de lógica pueden ser implementados usando arquitecturas de software contemporáneas. 

**Para estudiantes**: Proporciona una forma interactiva y moderna de dominar conceptos que son fundamento de la ciencia computacional.

**Para educadores**: Ofrece una herramienta pedagógica robusta, bien documentada y técnicamente sólida.

**Para desarrolladores**: Ilustra best practices en desarrollo web, testing, y arquitectura de software.

---

**¡Explora el fascinante mundo de la lógica formal con esta herramienta interactiva y educativamente fundamentada! 🎓🧠✨**