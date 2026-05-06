# 🌿 Biótica Consultores — Asistente IA de Calificación de Leads

Sistema completo de atención al cliente con IA para una consultora ambiental. Califica leads automáticamente, extrae información técnica y notifica por correo al equipo consultor.

---

## 🏗️ Arquitectura

```
Hackaton_Biotica/
├── backend_api.py        # API REST FastAPI (puerto 8000)
├── core/
│   ├── controller.py     # Lógica de negocio central
│   ├── llm_engine.py     # Motor IA (Groq / LLaMA 3.3)
│   ├── notifier.py       # Envío de correos Gmail + Excel
│   ├── prompts.py        # System prompt del asistente
│   └── utils.py          # Utilidades de parsing JSON
├── database/
│   └── db_manager.py     # SQLite con encriptación Fernet
├── frontend/             # Vue 3 (puerto 8081)
│   └── src/
│       ├── views/        # Home, Chat, Login, Admin
│       ├── components/   # ChatBox, ChatInput, ChatMessage...
│       ├── services/     # api.js, chat.service, admin.service
│       └── store/        # Vuex — estado global
├── .env                  # Variables de entorno (NO subir)
├── requirements.txt      # Dependencias Python
└── start.bat             # Script para levantar todo junto
```

---

## ⚙️ Requisitos previos

- Python 3.10+
- Node.js 18+
- Cuenta en [Groq](https://console.groq.com/) (API Key gratuita)
- Cuenta Gmail con [contraseña de aplicación](https://myaccount.google.com/apppasswords) habilitada

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Hackaton_Biotica.git
cd Hackaton_Biotica
```

### 2. Crear entorno virtual e instalar dependencias Python

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con este contenido:

```env
# IA
GROQ_API_KEY=tu_clave_de_groq

# Admin panel
ADMIN_USER=admin
ADMIN_PASSWORD=tu_password_seguro

# Correo (Gmail)
SMTP_USER=tucorreo@gmail.com
SMTP_PASS=xxxx xxxx xxxx xxxx
EMAIL_DESTINO=secretaria@tuempresa.com

# Encriptación DB (genera una clave con el comando de abajo)
ENCRYPT_KEY=
```

Para generar la `ENCRYPT_KEY`:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. Instalar dependencias del frontend

```bash
cd frontend
npm install
cd ..
```

---

## ▶️ Correr el proyecto

### Opción A — Script automático (recomendado)

Doble clic en `start.bat` — abre dos terminales automáticamente.

### Opción B — Manual

**Terminal 1 — Backend:**
```bash
venv\Scripts\activate
uvicorn backend_api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run serve
```


---

## 🌐 URLs

| Servicio | URL |
|----------|-----|
| Frontend (chat + admin) | http://localhost:8081 |
| Backend API | http://localhost:8000 |
| Documentación API (Swagger) | http://localhost:8000/docs |

---

## 🔐 Acceso al panel admin

1. Ir a `http://localhost:8081/login`
2. Usuario: el valor de `ADMIN_USER` en `.env`
3. Contraseña: el valor de `ADMIN_PASSWORD` en `.env`

El panel incluye:
- 📊 Indicadores de desempeño con gráficas
- 📋 Tabla de leads calificados con filtros
- 🗨️ Historial de conversaciones por sesión
- 📥 Exportación a Excel y CSV

---

## 🗄️ Base de datos

SQLite local en `biotica_hackathon.db`. Tres tablas:

| Tabla | Contenido |
|-------|-----------|
| `solicitudes` | Leads calificados (nombre y contacto encriptados) |
| `sesiones` | Registro de sesiones de chat |
| `historial_chat` | Mensajes completos por sesión |

Para inspeccionar la DB directamente, usa [DB Browser for SQLite](https://sqlitebrowser.org/).

---

## 📧 Correos automáticos

Cuando un lead es calificado (`es_finalizado: true`) o tiene urgencia alta, el sistema envía automáticamente un correo HTML a `EMAIL_DESTINO` con un Excel adjunto.

Requiere una **contraseña de aplicación** de Gmail (no la contraseña normal):
1. Activa verificación en 2 pasos en tu cuenta Google
2. Ve a: Cuenta → Seguridad → Contraseñas de aplicaciones
3. Genera una para "Correo / Windows"
4. Pega las 16 letras en `SMTP_PASS` del `.env`

---

## 🛠️ Stack tecnológico

**Backend:**
- FastAPI 0.111 + Uvicorn
- Groq API (LLaMA 3.3 70B Versatile)
- SQLite + Fernet (cryptography)
- Pandas + OpenPyXL

**Frontend:**
- Vue 3 + Vue Router + Vuex
- Axios (proxy a :8000)
- Bootstrap 5

---

---

## 👩‍💻 Autores

Desarrollado para Hackathon — Biótica Consultores  
Floridablanca, Santander · Colombia
