# 🎙️ Analizador de Reuniones AI

Una herramienta inteligente para transcribir, resumir y analizar el sentimiento de tus reuniones de trabajo utilizando Inteligencia Artificial de vanguardia.

## 🚀 Características
- **Transcripción Precisa**: Usa `OpenAI Whisper` para convertir audio a texto.
- **Resumen Inteligente**: Genera títulos, temas, decisiones y planes de acción usando `Google Gemini 2.0 Flash Lite`.
- **Análisis de Sentimiento**: Evalúa el tono emocional de la reunión (Productivo, Tenso, Neutral).
- **Asistente Conversacional**: Chat interactivo para preguntar detalles específicos sobre la reunión analizada.
- **Grabación Directa**: Captura audio desde el navegador o sube archivos existentes.

## 🛠️ Requisitos Previos
1. **Python 3.10+** instalado.
2. **FFmpeg**: Necesario para el procesamiento de audio.
   - *Nota*: El sistema está configurado para buscarlo en una ruta específica de Windows, pero se recomienda tenerlo en el PATH del sistema.

## 📦 Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clonar el repositorio
```bash
git clone https://github.com/CristoRodriguez1/analizador-reuniones.git
cd analizador-reuniones
```

### 2. Crear entorno virtual
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar dependencias
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo llamado `.env` en la raíz del proyecto (puedes usar `.env.example` como base):
```env
GEMINI_API_KEY=tu_clave_de_google_ai_studio
WHISPER_MODEL=base
MAX_AUDIO_DURATION_SECONDS=600
```
> **IMPORTANTE**: Nunca compartas tu `GEMINI_API_KEY` ni la subas a repositorios públicos.

## 🏃 Ejecución
Para iniciar el servidor de desarrollo:
```powershell
uvicorn app.main:app --reload
```
Luego, abre tu navegador en: [http://localhost:8000](http://localhost:8000)

## 📁 Estructura del Proyecto
- `app/`: Lógica principal (FastAPI, Pipeline de IA, Bot).
- `static/`: Archivos CSS y recursos estáticos.
- `temp_audio/`: Carpeta temporal para procesar grabaciones (se limpia automáticamente).
- `requirements.txt`: Lista de librerías necesarias.

## 💡 Notas de Desarrollo
- El sistema utiliza el nuevo SDK de `google-genai`.
- Se ha implementado un patrón Singleton para la carga de Whisper, optimizando el uso de memoria.
- Las tareas pesadas se ejecutan en un `executor` para no bloquear el servidor.

---
Desarrollado con ❤️ usando FastAPI y Google Gemini.
