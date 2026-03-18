"""
backend_api.py  ·  Biótica Consultores v2
==========================================
API REST completa:
  ✅ Chat con historial persistente en SQLite
  ✅ Login admin con Bearer token
  ✅ Indicadores de desempeño (gráficos)
  ✅ Exportar Excel (.xlsx) y CSV
  ✅ Historial de sesiones de chat
  ✅ CORS para Vue en :8081

Ejecutar:
    uvicorn backend_api:app --host 0.0.0.0 --port 8000 --reload
"""

import io
import os
import secrets
from datetime import datetime
from typing import List, Optional

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from core.controller import ejecutar_logica_backend
from database.db_manager import (
    init_db,
    obtener_todas_las_solicitudes,
    guardar_mensaje_historial,
    obtener_historial_sesion,
    obtener_sesiones,
    guardar_sesion,
)

# ─────────────────────────────────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(title="Biótica Consultores API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://0.0.0.0:8081",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Session-Id"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Auth — token en memoria (simple y sin dependencias extra)
# ─────────────────────────────────────────────────────────────────────────────
ADMIN_USER     = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "biotica2025")
_tokens: dict[str, str] = {}   # token → usuario


def _nuevo_token(usuario: str) -> str:
    token = secrets.token_hex(32)
    _tokens[token] = usuario
    return token


def verificar_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato: Bearer <token>")
    token = authorization.split(" ", 1)[1]
    if token not in _tokens:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return _tokens[token]


# ─────────────────────────────────────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────────────────────────────────────
class MensajeSchema(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MensajeSchema]
    lead_temp: Optional[dict] = None
    session_id: Optional[str] = None

class LoginRequest(BaseModel):
    usuario: str
    password: str


# ─────────────────────────────────────────────────────────────────────────────
# Startup
# ─────────────────────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    init_db()
    print("✅  Base de datos lista.")


# ─────────────────────────────────────────────────────────────────────────────
# Sistema
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# ─────────────────────────────────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/admin/login", tags=["Admin"])
def login(req: LoginRequest):
    if req.usuario != ADMIN_USER or req.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = _nuevo_token(req.usuario)
    return {"token": token, "usuario": req.usuario}


@app.post("/api/admin/logout", tags=["Admin"])
def logout(authorization: str = Header(...), _: str = Depends(verificar_token)):
    token = authorization.split(" ", 1)[1]
    _tokens.pop(token, None)
    return {"mensaje": "Sesión cerrada correctamente"}


# ─────────────────────────────────────────────────────────────────────────────
# Chat
# ─────────────────────────────────────────────────────────────────────────────
@app.post("/api/chat", tags=["Chat"])
def chat(req: ChatRequest):
    """
    Procesa el mensaje y guarda el historial en SQLite por session_id.
    Cumple: Interacción en tiempo real + Registro y almacenamiento.
    """
    try:
        t_inicio = datetime.now()

        historial = [{"role": m.role, "content": m.content} for m in req.messages]

        lead_temp = req.lead_temp or {
            "nombre": "N/A", "contacto": "N/A",
            "proyecto": "N/A", "ubicacion": "N/A", "info_tecnica": "",
        }
        lead_temp.setdefault("info_tecnica", "")

        # Crear/registrar sesión
        session_id = req.session_id or secrets.token_hex(8)
        guardar_sesion(session_id)

        # Guardar último mensaje del usuario
        ultimo_user = next((m for m in reversed(req.messages) if m.role == "user"), None)
        if ultimo_user:
            guardar_mensaje_historial(session_id, "user", ultimo_user.content)

        # Lógica principal (IA + DB)
        resultado, lead_actualizado, fue_guardado = ejecutar_logica_backend(
            historial_mensajes=historial,
            lead_temp=lead_temp,
        )

        # Guardar respuesta del bot
        guardar_mensaje_historial(session_id, "assistant", resultado.get("respuesta_bot", ""))

        t_ms = int((datetime.now() - t_inicio).total_seconds() * 1000)

        return {
            **resultado,
            "es_finalizado": bool(resultado.get("es_finalizado", False)),
            "lead_actualizado": lead_actualizado,
            "fue_guardado": fue_guardado,
            "session_id": session_id,
            "tiempo_respuesta_ms": t_ms,
        }

    except Exception as e:
        print(f"[ERROR /api/chat] {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# Historial de sesiones (admin)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/admin/sesiones", tags=["Admin"])
def get_sesiones(_: str = Depends(verificar_token)):
    return {"sesiones": obtener_sesiones()}


@app.get("/api/admin/sesiones/{session_id}", tags=["Admin"])
def get_historial_chat(session_id: str, _: str = Depends(verificar_token)):
    mensajes = obtener_historial_sesion(session_id)
    return {"session_id": session_id, "mensajes": mensajes}


# ─────────────────────────────────────────────────────────────────────────────
# Leads (admin)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/admin/leads", tags=["Admin"])
def get_leads(
    urgencia: Optional[str] = Query(None, description="Alta | Normal"),
    limite: int = Query(200, ge=1, le=1000),
    _: str = Depends(verificar_token),
):
    df = obtener_todas_las_solicitudes()
    if df.empty:
        return {"metricas": _metricas_vacias(), "leads": []}

    metricas = _calcular_metricas(df)

    if urgencia:
        df = df[df["urgencia"].str.lower() == urgencia.lower()]

    return {
        "metricas": metricas,
        "leads": df.head(limite).to_dict(orient="records"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Indicadores de desempeño (gráficos)
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/admin/stats", tags=["Admin"])
def get_stats(_: str = Depends(verificar_token)):
    """
    Indicadores para los gráficos del dashboard:
      - Solicitudes por servicio (clasificación)
      - Solicitudes por urgencia
      - Solicitudes por día (últimos 30 días)
      - % solicitudes filtradas (Fuera de alcance)
      - % urgentes
    Cumple: Generación de indicadores de desempeño.
    """
    df = obtener_todas_las_solicitudes()
    if df.empty:
        return _stats_vacias()

    # Por clasificación
    vc = df["clasificacion"].value_counts()
    por_clasificacion = [{"servicio": k, "total": int(v)} for k, v in vc.items()]

    # Por urgencia
    vu = df["urgencia"].value_counts()
    por_urgencia = [{"nivel": k, "total": int(v)} for k, v in vu.items()]

    # Por día
    df["fecha_dt"] = pd.to_datetime(df["fecha"], errors="coerce")
    df_ok = df.dropna(subset=["fecha_dt"])
    por_dia_raw = (
        df_ok.groupby(df_ok["fecha_dt"].dt.date).size().reset_index()
    )
    por_dia_raw.columns = ["fecha", "total"]
    por_dia = [
        {"fecha": str(r["fecha"]), "total": int(r["total"])}
        for _, r in por_dia_raw.tail(30).iterrows()
    ]

    total = len(df)
    fuera  = int(len(df[df["clasificacion"].str.lower() == "fuera de alcance"]))
    urgentes = int(len(df[df["urgencia"] == "Alta"]))

    return {
        "por_clasificacion": por_clasificacion,
        "por_urgencia": por_urgencia,
        "por_dia": por_dia,
        "pct_filtradas": round(fuera / total * 100, 1) if total else 0,
        "pct_urgentes": round(urgentes / total * 100, 1) if total else 0,
        "total_leads": total,
        "fuera_alcance": fuera,
        "urgentes": urgentes,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Exportación
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/api/admin/export/excel", tags=["Admin"])
def export_excel(_: str = Depends(verificar_token)):
    """Exporta leads + resumen a Excel (.xlsx) con dos hojas."""
    df = obtener_todas_las_solicitudes()
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay datos para exportar.")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Solicitudes")
        resumen = pd.DataFrame([_calcular_metricas(df)])
        resumen.to_excel(writer, index=False, sheet_name="Resumen")

    output.seek(0)
    filename = f"biotica_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/api/admin/export/csv", tags=["Admin"])
def export_csv(_: str = Depends(verificar_token)):
    """Exporta leads a CSV."""
    df = obtener_todas_las_solicitudes()
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay datos para exportar.")

    stream = io.StringIO()
    df.to_csv(stream, index=False, encoding="utf-8")
    stream.seek(0)
    filename = f"biotica_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _calcular_metricas(df: pd.DataFrame) -> dict:
    total = len(df)
    return {
        "total_leads": total,
        "urgencia_alta": int((df["urgencia"] == "Alta").sum()),
        "listos_para_consultor": int((df["siguiente_paso"] == "LISTO PARA CONSULTOR").sum()),
        "fuera_de_alcance": int(df["clasificacion"].str.lower().eq("fuera de alcance").sum()),
        "seguimiento_urgente": int((df["siguiente_paso"] == "SEGUIMIENTO URGENTE").sum()),
    }


def _metricas_vacias() -> dict:
    return {k: 0 for k in ["total_leads", "urgencia_alta", "listos_para_consultor",
                            "fuera_de_alcance", "seguimiento_urgente"]}


def _stats_vacias() -> dict:
    return {"por_clasificacion": [], "por_urgencia": [], "por_dia": [],
            "pct_filtradas": 0, "pct_urgentes": 0, "total_leads": 0,
            "fuera_alcance": 0, "urgentes": 0}