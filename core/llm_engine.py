"""
core/llm_engine.py  ·  Biótica Consultores
==========================================
Motor de IA.  Inyecta automáticamente la hora actual de Colombia
al inicio del último mensaje del usuario para que el bot pueda
validar el horario de atención.
"""

import os
import json
from datetime import datetime, timezone, timedelta

from openai import OpenAI
from dotenv import load_dotenv

from core.prompts import SYSTEM_PROMPT

# Cargar las variables del .env
load_dotenv()

# Conectamos directamente a los servidores ultra-rápidos de Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

<<<<<<< Updated upstream
def procesar_mensaje(mensaje_usuario):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Modelo premium gratis y rapidísimo
            response_format={"type": "json_object"}, # Groq soporta JSON estricto
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nREGLA: Responde estrictamente con un JSON válido."},
                {"role": "user", "content": mensaje_usuario}
            ],
            temperature=0.1
        )
        
        # Parseamos el JSON
=======
MAX_HISTORIAL = 6

# Zona horaria Colombia (UTC-5, sin cambio de horario)
TZ_COL = timezone(timedelta(hours=-5))

# Mapeo día inglés → español para el mensaje al usuario
DIAS_ES = {
    "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles",
    "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo"
}


def _hora_colombia() -> str:
    """Devuelve string tipo: 'Monday 09:35' en hora Colombia."""
    ahora = datetime.now(TZ_COL)
    dia   = ahora.strftime("%A")   # English day name (para la IA)
    hora  = ahora.strftime("%H:%M")
    return f"{dia} {hora}"


def procesar_mensaje(historial_mensajes: list) -> dict:
    """
    Recibe el historial y devuelve el JSON de la IA.
    Inyecta [HORA_ACTUAL: ...] en el último mensaje del usuario.
    """
    try:
        hora_tag = f"[HORA_ACTUAL: {_hora_colombia()}]"

        mensajes_ia = [{"role": "system", "content": SYSTEM_PROMPT}]

        ultimos = historial_mensajes[-MAX_HISTORIAL:]

        for i, m in enumerate(ultimos):
            content = m["content"]
            # Inyectamos la hora solo en el ÚLTIMO mensaje del usuario
            if m["role"] == "user" and i == len(ultimos) - 1:
                content = f"{hora_tag}\n{content}"
            mensajes_ia.append({"role": m["role"], "content": content})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            messages=mensajes_ia,
            temperature=0.1,
            max_tokens=800,
        )

>>>>>>> Stashed changes
        return json.loads(response.choices[0].message.content)

    except json.JSONDecodeError as e:
        print(f"[llm_engine] JSON parse error: {e}")
        return _fallback()
    except Exception as e:
<<<<<<< Updated upstream
        error_real = str(e)
        print(f"Error en Groq: {error_real}")
        return {
            "clasificacion": "Error de conexión",
            "urgencia": "Normal",
            "respuesta_bot": f"Detalle del error: {error_real}"
        }
=======
        print(f"[llm_engine] Groq error: {e}")
        return _fallback()


def _fallback() -> dict:
    return {
        "clasificacion": "Error",
        "urgencia": "Normal",
        "nombre_extraido": "No proporcionado",
        "contacto_extraido": "No proporcionado",
        "proyecto_nombre": "N/A",
        "ubicacion": "N/A",
        "informacion_recibida": "",
        "siguiente_paso": "Reintentar",
        "respuesta_bot": "Lo siento, tuve un problema de conexión. ¿Podrías repetir tu mensaje?",
        "es_finalizado": False,
    }
>>>>>>> Stashed changes
