import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from core.prompts import SYSTEM_PROMPT

# Cargar las variables del .env
load_dotenv()

# Conectamos directamente a los servidores ultra-rápidos de Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

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
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        error_real = str(e)
        print(f"Error en Groq: {error_real}")
        return {
            "clasificacion": "Error de conexión",
            "urgencia": "Normal",
            "respuesta_bot": f"Detalle del error: {error_real}"
        }