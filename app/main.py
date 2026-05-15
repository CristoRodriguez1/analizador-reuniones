import os
import uuid
import shutil
import aiofiles
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv

# Importaciones locales
from app.pipeline import transcribe_audio, analyze_with_gemini, analyze_sentiment
from app.bot import create_session, chat, get_history

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Analizador de Reuniones")

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
TEMP_AUDIO_DIR = os.path.join(BASE_DIR, "temp_audio")

# Crear carpeta temporal si no existe
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

# Montar estáticos y plantillas
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/")
async def index(request: Request):
    """
    Ruta principal que sirve la interfaz web.
    """
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze")
async def analyze(audio: UploadFile = File(...)):
    """
    Recibe un audio, lo procesa y devuelve el análisis completo.
    """
    session_id = str(uuid.uuid4())
    file_extension = audio.filename.split(".")[-1] if "." in audio.filename else "webm"
    temp_file_path = os.path.join(TEMP_AUDIO_DIR, f"{session_id}.{file_extension}")
    
    try:
        # Guardar archivo temporalmente
        async with aiofiles.open(temp_file_path, 'wb') as out_file:
            content = await audio.read()
            await out_file.write(content)
        
        # Ejecutar tareas pesadas en un ejecutor para no bloquear el event loop
        loop = asyncio.get_event_loop()
        
        # 1. Transcripción
        transcription = await loop.run_in_executor(None, transcribe_audio, temp_file_path)
        
        # 2. Análisis con Gemini
        analysis = await loop.run_in_executor(None, analyze_with_gemini, transcription)
        
        # 3. Análisis de sentimiento
        sentiment = await loop.run_in_executor(None, analyze_sentiment, transcription)
        
        # 4. Crear sesión de bot
        create_session(session_id, transcription, analysis)
        
        # Eliminar archivo temporal
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {
            "session_id": session_id,
            "transcription": transcription,
            "analysis": analysis,
            "sentiment": sentiment
        }
        
    except Exception as e:
        # Limpieza en caso de error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(data: dict = Body(...)):
    """
    Endpoint para interactuar con el bot.
    """
    session_id = data.get("session_id")
    message = data.get("message")
    
    if not session_id or not message:
        raise HTTPException(status_code=400, detail="Faltan datos (session_id o message)")
    
    try:
        response = await chat(session_id, message)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
async def history_endpoint(session_id: str):
    """
    Retorna el historial de conversación.
    """
    history = get_history(session_id)
    return history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
