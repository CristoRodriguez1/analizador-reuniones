import os
import json
from google import genai
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Configuración de Gemini para el chat con el nuevo SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Estado en memoria
sessions: Dict[str, Dict[str, Any]] = {}

def create_session(session_id: str, transcription: str, analysis: Dict[str, Any]):
    """
    Crea una nueva sesión de chat con la transcripción y el análisis de la reunión.
    """
    sessions[session_id] = {
        "transcription": transcription,
        "analysis": analysis,
        "history": []
    }

async def chat(session_id: str, user_message: str) -> str:
    """
    Maneja la interacción con el bot conversacional usando Gemini.
    """
    if session_id not in sessions:
        raise ValueError("La sesión no existe")
    
    session = sessions[session_id]
    transcription = session["transcription"]
    analysis_json = json.dumps(session["analysis"], indent=2, ensure_ascii=False)
    
    # Agregar mensaje del usuario al historial
    session["history"].append({"role": "user", "content": user_message})
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Construir el prompt de sistema y contexto
        system_prompt = f"""
Eres un asistente conversacional experto en análisis de reuniones. Tienes acceso al análisis completo de una reunión y a su transcripción original.

Análisis de la reunión:
{analysis_json}

Transcripción original:
{transcription}

Responde las preguntas del usuario de forma clara y concisa basándote únicamente en la información de esta reunión. Si algo no aparece en la transcripción, dilo explícitamente.
"""
        
        # Convertir historial para Gemini
        # Gemini espera roles 'user' y 'model'
        history = []
        for msg in session["history"][:-1]: # No incluimos el último mensaje del usuario aún
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})
        
        # Determinar el mensaje a enviar: incluir contexto solo en el primer turno
        if not history:
            message_to_send = f"{system_prompt}\n\nPrimera pregunta del usuario: {user_message}"
        else:
            message_to_send = user_message
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=message_to_send
        )
        assistant_response = response.text.strip()
        
        # Agregar respuesta al historial
        session["history"].append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
        
    except Exception as e:
        error_msg = f"Error en el chat: {str(e)}"
        session["history"].append({"role": "assistant", "content": error_msg})
        return error_msg

def get_history(session_id: str) -> List[Dict[str, str]]:
    """
    Retorna el historial de la sesión.
    """
    if session_id in sessions:
        return sessions[session_id]["history"]
    return []
