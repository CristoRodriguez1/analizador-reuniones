import os
import json
import whisper
import google.generativeai as genai
from transformers import pipeline
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Configuración de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Singleton para Whisper
_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        model_name = os.getenv("WHISPER_MODEL", "base")
        _whisper_model = whisper.load_model(model_name)
    return _whisper_model

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe el archivo de audio usando OpenAI Whisper.
    """
    try:
        model = get_whisper_model()
        result = model.transcribe(file_path)
        return result["text"].strip()
    except Exception as e:
        raise ValueError(f"Error al transcribir el audio: {str(e)}")

def analyze_with_gemini(transcription: str) -> Dict[str, Any]:
    """
    Analiza la transcripción usando Google Gemini 1.5 Flash.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
Eres un asistente experto en análisis de reuniones de trabajo. Analiza la siguiente transcripción y responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, sin explicaciones, sin bloques de código markdown.

El JSON debe tener exactamente esta estructura:
{{
  "titulo": "título descriptivo de la reunión",
  "participantes": ["nombre1", "nombre2"],
  "temas": ["tema 1", "tema 2", "tema 3"],
  "decisiones": ["decisión 1", "decisión 2"],
  "acciones": [
    {{"tarea": "descripción de la tarea", "responsable": "nombre o desconocido", "plazo": "fecha o no especificado"}}
  ],
  "resumen": "resumen ejecutivo de máximo 5 líneas de la reunión"
}}

Transcripción:
{transcription}
"""
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Limpiar bloques de código markdown si existen
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "", 1)
        if text_response.endswith("```"):
            text_response = text_response.rsplit("```", 1)[0]
        
        text_response = text_response.strip()
        
        try:
            return json.loads(text_response)
        except json.JSONDecodeError:
            return {"error": "Error al parsear el JSON de Gemini", "raw_response": text_response}
            
    except Exception as e:
        return {"error": f"Error en la comunicación con Gemini: {str(e)}"}

def analyze_sentiment(transcription: str) -> Dict[str, Any]:
    """
    Analiza el sentimiento de la reunión usando un modelo de Hugging Face.
    """
    try:
        # Usamos el pipeline de transformers con el modelo indicado
        sentiment_pipeline = pipeline(
            "sentiment-analysis", 
            model="pysentimiento/robertuito-sentiment-analysis"
        )
        
        # Dividir la transcripción en fragmentos de máximo 400 caracteres
        chunks = [transcription[i:i+400] for i in range(0, len(transcription), 400)]
        
        if not chunks:
            return {
                "etiqueta": "NEU",
                "descripcion": "Neutral",
                "scores": {"POS": 0.0, "NEG": 0.0, "NEU": 1.0}
            }

        all_results = sentiment_pipeline(chunks)
        
        # Promediar los scores
        # El modelo Robertuito suele devolver etiquetas como 'POS', 'NEG', 'NEU'
        avg_scores = {"POS": 0.0, "NEG": 0.0, "NEU": 0.0}
        
        for chunk_results in all_results:
            for res in chunk_results:
                label = res['label'].upper()
                if label in avg_scores:
                    avg_scores[label] += res['score']
        
        num_chunks = len(chunks)
        for label in avg_scores:
            avg_scores[label] /= num_chunks
            
        # Determinar etiqueta dominante
        dominant_label = max(avg_scores, key=avg_scores.get)
        
        descriptions = {
            "POS": "Productiva",
            "NEG": "Tensa",
            "NEU": "Neutral"
        }
        
        return {
            "etiqueta": dominant_label,
            "descripcion": descriptions.get(dominant_label, "Neutral"),
            "scores": avg_scores
        }
    except Exception as e:
        # Fallback en caso de error (modelo no descargado, etc)
        return {
            "etiqueta": "NEU",
            "descripcion": f"Error en análisis: {str(e)}",
            "scores": {"POS": 0.0, "NEG": 0.0, "NEU": 0.0}
        }
