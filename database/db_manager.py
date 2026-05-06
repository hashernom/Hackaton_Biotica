"""
database/db_manager.py  ·  Biótica Consultores
===============================================
Gestiona SQLite.  Los campos sensibles del cliente
(nombre, contacto) se almacenan encriptados con Fernet
(AES-128-CBC + HMAC-SHA256) — reversible para mostrarlos
en el panel admin.

bcrypt NO se usa aquí porque es unidireccional (no se puede
desencriptar). Usamos Fernet (cryptography) que es simétrico,
seguro y permite leer los datos de vuelta.

Genera la clave una sola vez:
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
Y guárdala en .env como:  ENCRYPT_KEY=xxxxxxx...
"""

import os
import sqlite3
from datetime import datetime
from typing import List

import pandas as pd
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "biotica_hackathon.db")

# ── Clave de encriptación ─────────────────────────────────────────────────
# Si no está configurada, genera una temporal (solo para desarrollo).
_raw_key = os.getenv("ENCRYPT_KEY", "")
if _raw_key:
    _fernet = Fernet(_raw_key.encode())
else:
    # Clave temporal: genera una nueva cada vez que arranca (solo DEV)
    _temp_key = Fernet.generate_key()
    _fernet   = Fernet(_temp_key)
    print(
        "[db_manager] [WARN] ENCRYPT_KEY no configurada. "
        "Generando clave temporal (los datos no serán recuperables entre reinicios)."
    )
    print(f"  Anade esto a tu .env:\n  ENCRYPT_KEY={_temp_key.decode()}")


def _enc(texto: str) -> str:
    """Encripta un string y devuelve el token como string UTF-8."""
    if not texto or texto in ("N/A", "No proporcionado", ""):
        return texto
    return _fernet.encrypt(texto.encode()).decode()


def _dec(token: str) -> str:
    """Desencripta un token Fernet. Si falla (datos sin encriptar), devuelve el original."""
    if not token or token in ("N/A", "No proporcionado", ""):
        return token
    try:
        return _fernet.decrypt(token.encode()).decode()
    except (InvalidToken, Exception):
        return token  # datos legacy sin encriptar


# ─────────────────────────────────────────────────────────────────────────────
# Conexión
# ─────────────────────────────────────────────────────────────────────────────
def _conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# Inicialización
# ─────────────────────────────────────────────────────────────────────────────
def init_db() -> None:
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha           TEXT NOT NULL,
                nombre          TEXT,
                contacto        TEXT,
                proyecto        TEXT,
                ubicacion       TEXT,
                mensaje_usuario TEXT,
                clasificacion   TEXT,
                urgencia        TEXT,
                info_tecnica    TEXT,
                siguiente_paso  TEXT
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS sesiones (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                creada_en  TEXT NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS historial_chat (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role       TEXT NOT NULL,
                content    TEXT NOT NULL,
                timestamp  TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sesiones(session_id)
            )
        """)
        con.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Solicitudes — escribe encriptado, lee desencriptado
# ─────────────────────────────────────────────────────────────────────────────
def guardar_solicitud(
    nombre: str, contacto: str, proyecto: str, ubicacion: str,
    mensaje: str, clasificacion: str, urgencia: str,
    info_tecnica: str, siguiente_paso: str,
) -> int:
    """Guarda el lead.  nombre y contacto se encriptan antes de escribir."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as con:
        cur = con.execute(
            """INSERT INTO solicitudes
               (fecha, nombre, contacto, proyecto, ubicacion, mensaje_usuario,
                clasificacion, urgencia, info_tecnica, siguiente_paso)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                fecha,
                _enc(nombre),    # ← encriptado
                _enc(contacto),  # ← encriptado
                proyecto, ubicacion, mensaje,
                clasificacion, urgencia, info_tecnica, siguiente_paso,
            ),
        )
        con.commit()
        return cur.lastrowid


def obtener_todas_las_solicitudes() -> pd.DataFrame:
    """Devuelve todos los leads con nombre y contacto YA desencriptados."""
    with _conn() as con:
        df = pd.read_sql_query("SELECT * FROM solicitudes ORDER BY id DESC", con)
    if df.empty:
        return df
    df["nombre"]   = df["nombre"].apply(_dec)
    df["contacto"] = df["contacto"].apply(_dec)
    return df


def obtener_solicitud_por_id(solicitud_id: int) -> dict | None:
    with _conn() as con:
        cur = con.execute("SELECT * FROM solicitudes WHERE id = ?", (solicitud_id,))
        row = cur.fetchone()
        if not row:
            return None
        cols = [d[0] for d in cur.description]
        data = dict(zip(cols, row))
    data["nombre"]   = _dec(data["nombre"])
    data["contacto"] = _dec(data["contacto"])
    return data


# ─────────────────────────────────────────────────────────────────────────────
# Sesiones y historial
# ─────────────────────────────────────────────────────────────────────────────
def guardar_sesion(session_id: str) -> None:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as con:
        con.execute(
            "INSERT OR IGNORE INTO sesiones (session_id, creada_en) VALUES (?,?)",
            (session_id, fecha),
        )
        con.commit()


def obtener_sesiones() -> List[dict]:
    with _conn() as con:
        df = pd.read_sql_query(
            """SELECT s.session_id, s.creada_en,
                      COUNT(h.id) AS total_mensajes
               FROM sesiones s
               LEFT JOIN historial_chat h ON s.session_id = h.session_id
               GROUP BY s.session_id ORDER BY s.id DESC""",
            con,
        )
    return df.to_dict(orient="records") if not df.empty else []


def guardar_mensaje_historial(session_id: str, role: str, content: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as con:
        con.execute(
            "INSERT INTO historial_chat (session_id, role, content, timestamp) VALUES (?,?,?,?)",
            (session_id, role, content, ts),
        )
        con.commit()


def obtener_historial_sesion(session_id: str) -> List[dict]:
    with _conn() as con:
        df = pd.read_sql_query(
            "SELECT role, content, timestamp FROM historial_chat WHERE session_id=? ORDER BY id",
            con, params=(session_id,),
        )
    return df.to_dict(orient="records") if not df.empty else []