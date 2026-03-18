"""
core/controller.py  ·  Biótica Consultores
==========================================
Coordina el flujo principal del backend:
    IA  →  Actualizar memoria del lead  →  Guardar/Notificar si aplica

No contiene ninguna lógica de presentación (Streamlit, Vue, HTML, etc.).
"""

from core.llm_engine import procesar_mensaje
from database.db_manager import guardar_solicitud
from core.notifier import enviar_notificacion_lead


def ejecutar_logica_backend(historial_mensajes: list, lead_temp: dict) -> tuple:
    """
    Coordina todo el backend.

    Parámetros
    ----------
    historial_mensajes : list
        Lista de dicts con 'role' y 'content'. Viene del frontend Vue
        a través de la API.
    lead_temp : dict
        Estado actual del lead con claves:
        nombre, contacto, proyecto, ubicacion, info_tecnica.

    Retorna
    -------
    tuple: (resultado: dict, lead_temp: dict, se_guarda: bool)
        resultado    → JSON completo devuelto por la IA.
        lead_temp    → Lead actualizado con los datos extraídos.
        se_guarda    → True si el lead fue guardado en la DB en esta llamada.
    """

    # ── 1. Obtener respuesta de la IA ─────────────────────────────────────
    resultado = procesar_mensaje(historial_mensajes)

    # ── 2. Actualizar lead_temp con lo que encontró la IA ─────────────────
    nombre_ia   = resultado.get("nombre_extraido", "No proporcionado")
    contacto_ia = resultado.get("contacto_extraido", "No proporcionado")
    proyecto_ia = resultado.get("proyecto_nombre", "N/A")
    ubicacion_ia = resultado.get("ubicacion", "N/A")
    info_ia     = resultado.get("informacion_recibida", "")

    if nombre_ia and nombre_ia != "No proporcionado":
        lead_temp["nombre"] = nombre_ia

    if contacto_ia and contacto_ia != "No proporcionado":
        lead_temp["contacto"] = contacto_ia

    # Solo sobreescribimos si la IA encontró datos nuevos (no vacíos ni N/A)
    if proyecto_ia and proyecto_ia != "N/A":
        lead_temp["proyecto"] = proyecto_ia

    if ubicacion_ia and ubicacion_ia != "N/A":
        lead_temp["ubicacion"] = ubicacion_ia

    # Acumulamos el resumen técnico (evitamos duplicar entradas vacías)
    if info_ia:
        lead_temp["info_tecnica"] = (
            f"{lead_temp.get('info_tecnica', '')} | {info_ia}".strip(" |")
        )

    # ── 3. Decidir si guardar el lead en la DB ────────────────────────────
    es_finalizado = resultado.get("es_finalizado", False)
    es_urgente    = resultado.get("urgencia") == "Alta"
    se_guarda     = False

    if es_finalizado or es_urgente:
        siguiente_paso = "LISTO PARA CONSULTOR" if es_finalizado else "SEGUIMIENTO URGENTE"

        guardar_solicitud(
            nombre       = lead_temp["nombre"],
            contacto     = lead_temp["contacto"],
            proyecto     = lead_temp["proyecto"],
            ubicacion    = lead_temp["ubicacion"],
            mensaje      = historial_mensajes[-1]["content"] if historial_mensajes else "",
            clasificacion= resultado.get("clasificacion", "N/A"),
            urgencia     = resultado.get("urgencia", "Normal"),
            info_tecnica = lead_temp.get("info_tecnica", "N/A"),
            siguiente_paso = siguiente_paso,
        )

        # Notificación por correo (simulada en consola)
        enviar_notificacion_lead({
            "nombre"       : lead_temp["nombre"],
            "contacto"     : lead_temp["contacto"],
            "proyecto"     : lead_temp["proyecto"],
            "ubicacion"    : lead_temp["ubicacion"],
            "clasificacion": resultado.get("clasificacion", "N/A"),
            "urgencia"     : resultado.get("urgencia", "Normal"),
            "info_tecnica" : lead_temp.get("info_tecnica", ""),
            "siguiente_paso": siguiente_paso,
        })

        se_guarda = True

    return resultado, lead_temp, se_guarda