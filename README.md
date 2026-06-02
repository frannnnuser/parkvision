# 🅿️ ParkVision

Sistema inteligente de gestión y control de estacionamientos con reconocimiento automático de matrículas (LPR), cámara en tiempo real y dashboard web.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Reference](#api-reference)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)

---

## ✨ Características

| Módulo | Descripción |
|---|---|
| 📷 **Cámara Live** | Detección de movimiento por MOG2, soporte para webcam, cámara del navegador y cámaras IP/RTSP |
| 🔍 **Reconocimiento de Matrículas** | Integración con [PlateRecognizer API](https://platerecognizer.com/); modo simulación automático sin API key |
| 📊 **Dashboard en Tiempo Real** | Estadísticas de ocupación, donut chart, feed de eventos via SSE |
| 🗃️ **Gestión de Vehículos** | CRUD completo, marcado de vehículos autorizados/bloqueados |
| 🅿️ **Control de Espacios** | 30 espacios en 2 niveles (A y B), asignación y liberación automática |
| 📜 **Historial de Accesos** | Registro completo de entradas/salidas con confianza de reconocimiento y fuente |
| 📤 **Escáner Manual** | Upload de imagen o registro manual de matrícula |

---

## 🏗️ Arquitectura

```
ParkVision/
├── app/
│   ├── api/            # Blueprints REST (Flask)
│   │   ├── camera.py   # Stream MJPEG, SSE events, captura
│   │   ├── dashboard.py
│   │   ├── records.py  # Upload de imágenes, registro manual
│   │   ├── slots.py    # Espacios de estacionamiento
│   │   └── vehicles.py # CRUD vehículos
│   ├── models/         # SQLAlchemy ORM
│   │   ├── record.py   # ParkingRecord
│   │   ├── slot.py     # ParkingSlot
│   │   └── vehicle.py  # Vehicle
│   └── services/
│       ├── camera.py         # Captura OpenCV, detección de movimiento
│       ├── parking.py        # Lógica entrada/salida
│       └── plate_recognizer.py  # API + simulador
├── static/
│   ├── css/main.css
│   └── js/main.js      # SPA vanilla JS
├── templates/index.html
├── run.py
└── requirements.txt
```

**Flujo de detección automática:**

```
Cámara → Detección de Movimiento (MOG2/JS) → Captura de Frame
  → PlateRecognizer API (o simulador) → process_plate()
    → Asignar/liberar espacio → SSE push → Dashboard
```

---

## ⚙️ Requisitos

- Python 3.10+
- pip
- (Opcional) OpenCV — para modo webcam/IP del servidor
- (Opcional) API Key de [PlateRecognizer](https://app.platerecognizer.com/accounts/plan/) para reconocimiento real

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/parkvision.git
cd parkvision
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///parkvision.db
PLATE_RECOGNIZER_API_KEY=tu_api_key_aqui
CAMERA_COOLDOWN=8
FLASK_DEBUG=false
PORT=5000
```

> 💡 Si no tienes API key de PlateRecognizer, el sistema funciona en **modo demo** generando matrículas simuladas automáticamente.

### 5. Ejecutar

```bash
python run.py
```

Abre tu navegador en: **http://localhost:5000**

---

## 🔧 Configuración

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `SECRET_KEY` | Clave secreta Flask | `dev-secret` |
| `DATABASE_URL` | URI de base de datos | `sqlite:///parkvision.db` |
| `PLATE_RECOGNIZER_API_KEY` | API key de PlateRecognizer | `""` (modo simulación) |
| `CAMERA_COOLDOWN` | Segundos entre capturas automáticas | `8` |
| `FLASK_DEBUG` | Modo debug | `false` |
| `PORT` | Puerto del servidor | `5000` |

### Producción con Gunicorn

```bash
gunicorn run:app --workers 1 --threads 4 --bind 0.0.0.0:5000
```

> ⚠️ Usar `--workers 1` porque la cámara mantiene estado en memoria (singleton).

---

## 📖 Uso

### Dashboard
Vista principal con estadísticas de ocupación en tiempo real, gráfico donut y feed de los últimos eventos.

### Cámara Live
Soporta tres fuentes:
- **Cámara del Navegador** — Usa la webcam del dispositivo vía WebRTC. No requiere OpenCV.
- **Webcam del Servidor** — Captura desde una webcam conectada al servidor.
- **Cámara IP / RTSP** — Conecta con una URL `rtsp://` o `http://`.

La detección de movimiento activa la captura automáticamente según el cooldown configurado.

### Escáner
- Arrastra o sube una imagen de un vehículo para reconocer la matrícula.
- O ingresa la matrícula manualmente para registrar una entrada/salida.

### Vehículos
CRUD completo. Los vehículos pueden ser marcados como **Autorizados** o **Bloqueados**. Los bloqueados aparecen con alerta roja en cada detección.

### Planta del Parqueo
Vista visual de los 30 espacios distribuidos en 2 niveles (A01–A15 y B01–B15).

---

## 🔌 API Reference

### Dashboard

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/dashboard/stats` | Estadísticas generales |
| `GET` | `/api/dashboard/inside` | Vehículos actualmente dentro |

### Vehículos

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/vehicles/` | Listar todos |
| `POST` | `/api/vehicles/` | Crear vehículo |
| `GET` | `/api/vehicles/<id>` | Obtener por ID |
| `PATCH` | `/api/vehicles/<id>` | Actualizar |
| `DELETE` | `/api/vehicles/<id>` | Eliminar |

### Registros

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/records/` | Historial (param: `?limit=100`) |
| `POST` | `/api/records/upload` | Subir imagen para reconocimiento |
| `POST` | `/api/records/manual` | Registro manual de matrícula |

### Cámara

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/camera/start` | Iniciar cámara del servidor |
| `POST` | `/api/camera/stop` | Detener cámara |
| `GET` | `/api/camera/status` | Estado actual |
| `POST` | `/api/camera/capture` | Captura y reconocimiento manual |
| `GET` | `/api/camera/stream` | Stream MJPEG |
| `GET` | `/api/camera/events` | SSE — eventos en tiempo real |

### Espacios

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/slots/` | Listar todos los espacios |

### Formato de respuesta

```json
{
  "ok": true,
  "data": { ... }
}
```

```json
{
  "ok": false,
  "error": "Mensaje de error"
}
```

---

## 📁 Estructura del Proyecto

```
parkvision/
├── app/
│   ├── __init__.py           # App factory, seed inicial
│   ├── api/
│   │   ├── __init__.py
│   │   ├── _helpers.py       # success(), error(), validate_json()
│   │   ├── camera.py
│   │   ├── dashboard.py
│   │   ├── records.py
│   │   ├── slots.py
│   │   └── vehicles.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── record.py         # ParkingRecord
│   │   ├── slot.py           # ParkingSlot (assign/release)
│   │   └── vehicle.py        # Vehicle
│   └── services/
│       ├── __init__.py
│       ├── camera.py         # Singleton de cámara + MOG2
│       ├── parking.py        # process_plate(), get_stats()
│       └── plate_recognizer.py
├── instance/
│   └── parkvision.db         # Base de datos SQLite (auto-generada)
├── static/
│   ├── css/main.css
│   ├── js/main.js
│   └── uploads/              # Imágenes capturadas
├── templates/
│   └── index.html            # SPA única página
├── .env                      # Variables de entorno (no commitear)
├── .gitignore
├── requirements.txt
└── run.py
```

---

## 🛠️ Tecnologías

**Backend**
- [Flask 3.x](https://flask.palletsprojects.com/) — Framework web
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) — Migraciones de BD
- [OpenCV](https://opencv.org/) — Captura de video y detección de movimiento
- [Pillow](https://pillow.readthedocs.io/) — Procesamiento de imágenes
- [PlateRecognizer API](https://platerecognizer.com/) — Reconocimiento de matrículas

**Frontend**
- HTML5 + CSS3 + JavaScript (Vanilla, sin frameworks)
- [Bootstrap 5.3](https://getbootstrap.com/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)
- Server-Sent Events (SSE) para tiempo real

**Base de Datos**
- SQLite (desarrollo) — reemplazable por PostgreSQL/MySQL vía `DATABASE_URL`

---

## 📝 Notas

- La base de datos se crea automáticamente al primer inicio con 30 espacios y 5 vehículos de ejemplo.
- El modo simulación genera matrículas aleatorias con formato `XXX-000` cuando no hay API key configurada.
- Las imágenes capturadas se guardan en `static/uploads/`.
- Agregar `static/uploads/` e `instance/` al `.gitignore` para no subir datos sensibles ni la BD al repositorio.