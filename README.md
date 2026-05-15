# Analizador de Reuniones

## Planteamiento del Problema
En el entorno laboral moderno, las reuniones son constantes y generan una gran cantidad de información. A menudo, los participantes pierden detalles importantes, las tareas asignadas no quedan claras o el sentimiento general de la reunión no se percibe de manera objetiva. La transcripción manual es tediosa y el análisis manual de largas grabaciones consume demasiado tiempo.

## Objetivo General
Desarrollar una herramienta integral que automatice el procesamiento de grabaciones de reuniones, proporcionando transcripciones precisas, resúmenes inteligentes, identificación de puntos clave (participantes, temas, decisiones, acciones) y un análisis de sentimiento, facilitando además la interacción con la información a través de un chat inteligente.

## Metodología
El proyecto sigue un flujo de procesamiento secuencial representado en el siguiente diagrama:

1. **Captura**: El usuario sube un archivo o graba directamente desde el navegador.
2. **Transcripción**: Se utiliza OpenAI Whisper para convertir el audio a texto.
3. **Análisis de Contenido**: Google Gemini 1.5 Flash procesa el texto para extraer entidades y estructurar el resumen.
4. **Análisis de Sentimiento**: Un modelo RoBERTuito especializado en español evalúa el tono de la reunión.
5. **Persistencia y Chat**: Se crea una sesión en memoria que permite al usuario realizar preguntas específicas sobre lo discutido.

*(El diagrama de flujo se encuentra conceptualmente integrado en este proceso de 5 pasos)*.

## Desarrollo
El sistema está construido con:
- **Backend**: FastAPI (Python) para una API de alto rendimiento.
- **Modelos de IA**: 
  - `openai-whisper` para procesamiento de audio.
  - `google-generativeai` para razonamiento avanzado.
  - `transformers` con `pysentimiento` para análisis emocional.
- **Frontend**: Vanilla JavaScript, HTML5 y CSS3 con diseño responsivo y moderno.

## Resultados
Se ha logrado una plataforma capaz de reducir el tiempo de post-procesamiento de una reunión de horas a solo un par de minutos. El usuario obtiene una visualización clara de las decisiones y un plan de acción inmediato, junto con una interfaz de chat para resolver dudas sin tener que volver a escuchar el audio.

## Discusión
La precisión del sistema depende en gran medida de la calidad del audio. Si bien Whisper es robusto, ruidos de fondo extremos pueden afectar la transcripción. El uso de Gemini 1.5 Flash ofrece un equilibrio óptimo entre velocidad y capacidad de análisis para estructurar los datos JSON requeridos.

---

## Instalación y Ejecución

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repo>
   cd analizador-reuniones
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   - Copia `.env.example` a `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edita `.env` y añade tu `GEMINI_API_KEY`.

5. **Correr la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Acceder**:
   Abre [http://localhost:8000](http://localhost:8000) en tu navegador.
