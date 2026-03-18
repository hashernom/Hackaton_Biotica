"""
core/utils.py  ·  Biótica Consultores
======================================
Utilidades generales del backend.
"""

import json
import re


def limpiar_y_cargar_json(texto_crudo: str) -> dict | None:
    """
    Extrae y valida el JSON incluso si la IA incluye texto extra alrededor.

    Parámetros
    ----------
    texto_crudo : str
        Texto devuelto por el modelo, que puede contener texto fuera del JSON.

    Retorna
    -------
    dict | None
        Diccionario parseado o None si no se pudo extraer un JSON válido.
    """
    if not texto_crudo:
        return None

    try:
        # Intento directo
        return json.loads(texto_crudo)
    except json.JSONDecodeError:
        pass

    # Busca el primer bloque {...} en el texto
    match = re.search(r"\{.*\}", texto_crudo, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            print(f"[utils] Error crítico de parsing JSON: {e}")

    return None