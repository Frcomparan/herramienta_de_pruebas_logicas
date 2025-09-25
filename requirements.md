***

### **Ticket: Herramienta de Pruebas Lógicas con Reglas de Inferencia**

* **ID del Ticket:** LOGIC-007
* **Tipo:** Feature (Nueva Funcionalidad)
* **Prioridad:** Alta

---

### ## Resumen

Se requiere desarrollar una aplicación web monolítica y contenerizada que permita a los usuarios introducir un argumento en lenguaje natural. La aplicación debe analizarlo, determinar su validez y, crucialmente, **generar una prueba deductiva paso a paso utilizando reglas de inferencia formales** (Modus Ponens, Modus Tollens, etc.) como justificación de su validez.

---

### ## User Story (Historia de Usuario)

**Como** un estudiante de lógica, **quiero** introducir un argumento en texto normal y no solo saber si es válido, sino también **ver la derivación lógica exacta, paso a paso**, que demuestra cómo la conclusión se sigue de las premisas, **para** poder comprender y aprender el proceso de razonamiento formal. 🧠

---

### ## Requisitos Funcionales y Criterios de Aceptación

#### **Interfaz y Flujo de Usuario**
* ✅ La página principal debe mostrar un formulario HTML con **dos campos de texto** para las premisas y un campo para la conclusión.
* ✅ El formulario debe incluir un botón o enlace para **"+ Añadir Premisa"**. Al hacer clic, la página se recarga mostrando un campo de entrada adicional.
* ✅ Al enviar el formulario con el botón "Validar", la página se recarga mostrando los resultados debajo del formulario.

#### **Procesamiento y Salida de Resultados**
* ✅ El backend debe procesar el texto de todas las premisas y la conclusión utilizando un servicio de **Procesamiento de Lenguaje Natural (PLN)**.
* ✅ El sistema debe traducir el argumento a su **forma simbólica**.
* ✅ El sistema debe determinar la validez del argumento. Para ello, debe ser capaz de reconocer y aplicar las **reglas de inferencia estándar** (Modus Ponens, Modus Tollens, Silogismo Hipotético, Conjunción, Silogismo Disyuntivo, Adición, Simplificación, etc.).
* ✅ La página de resultados debe mostrar claramente:
    1.  El estado final: **"Argumento Válido"** ✅ o **"Argumento Inválido"** ❌.
    2.  La traducción simbólica generada.
    3.  **Una justificación de la validez:**
        * Si el argumento es **válido**, se debe mostrar una **derivación paso a paso** que demuestre cómo se llega a la conclusión a partir de las premisas, nombrando las reglas de inferencia utilizadas en cada paso.
        * Si el argumento es **inválido**, se debe mostrar un **contraejemplo** (una asignación de valores de verdad donde las premisas son verdaderas y la conclusión es falsa).



---

### ## Arquitectura y Stack Tecnológico

* **Arquitectura:** **Aplicación Monolítica (Renderizado desde Servidor)**.
* **Lenguaje Principal:** **Python**.
* **Framework Backend:** **FastAPI**, por su naturaleza asíncrona y alto rendimiento.
* **Motor de Plantillas (Templates):** **Jinja2**, para generar el HTML dinámicamente desde FastAPI.
* **Interfaz de Usuario y Estilos:** **HTML5** con **Tailwind CSS** para un diseño moderno y responsivo.
* **Lógica Principal (PLN y Pruebas):** Integración con una API de un **Modelo de Lenguaje Grande (LLM)** como **Google Gemini**. El LLM será responsable de:
    1.  La interpretación del lenguaje natural a lógica simbólica.
    2.  **Generar la prueba de derivación paso a paso utilizando las reglas de inferencia estándar.**
* **Contenerización:** La aplicación completa debe estar contenida en una imagen de **Docker** para asegurar la portabilidad y facilitar el despliegue. 🐳