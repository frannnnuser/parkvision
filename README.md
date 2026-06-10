<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ParkVision — README</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<style>
  body { background: #f8f9fa; font-family: 'Segoe UI', system-ui, sans-serif; }
  .hero { background: #1a1d23; color: #fff; padding: 56px 0 40px; border-bottom: 3px solid #198754; }
  .hero .badge-tech { background: rgba(25,135,84,0.15); border: 1px solid rgba(25,135,84,0.3); color: #25d07a; font-size: 0.75rem; font-weight: 500; padding: 4px 10px; border-radius: 20px; }
  .hero .subtitle { color: #8892a4; font-size: 1rem; }
  .section-title { font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #6c757d; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #dee2e6; }
  .feature-card { background: #fff; border: 1px solid #dee2e6; border-left: 3px solid #198754; border-radius: 8px; padding: 16px 18px; height: 100%; }
  .feature-card .icon { width: 36px; height: 36px; border-radius: 8px; display: grid; place-items: center; font-size: 1rem; background: #f0fdf4; color: #198754; flex-shrink: 0; }
  .feature-card h6 { font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
  .feature-card p { font-size: 0.8rem; color: #6c757d; margin: 0; }
  .step-num { width: 28px; height: 28px; border-radius: 50%; background: #198754; color: #fff; display: grid; place-items: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; }
  .step-block { background: #fff; border: 1px solid #dee2e6; border-radius: 8px; padding: 18px 20px; }
  code, pre { font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 0.82rem; }
  pre { background: #1a1d23; color: #e8ecf4; border-radius: 8px; padding: 16px 18px; overflow-x: auto; }
  pre .c { color: #5a6070; }
  .env-block { background: #1a1d23; color: #e8ecf4; border-radius: 8px; padding: 16px 18px; font-family: monospace; font-size: 0.82rem; }
  .env-block .key { color: #25d07a; }
  .env-block .val { color: #ffc107; }
  .env-block .comment { color: #5a6070; }
  .toc-link { display: block; padding: 5px 12px; font-size: 0.82rem; color: #495057; text-decoration: none; border-radius: 4px; }
  .toc-link:hover { background: #f0fdf4; color: #198754; }
  .toc-link.active { background: #f0fdf4; color: #198754; font-weight: 600; border-left: 2px solid #198754; }
  .method-badge { font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 4px; font-family: monospace; }
  .method-get    { background: #d1ecf1; color: #0c5460; }
  .method-post   { background: #d4edda; color: #155724; }
  .method-patch  { background: #fff3cd; color: #856404; }
  .method-delete { background: #f8d7da; color: #721c24; }
  .endpoint { font-family: monospace; font-size: 0.82rem; color: #495057; }
  .tech-badge { background: #fff; border: 1px solid #dee2e6; border-radius: 6px; padding: 6px 12px; font-size: 0.8rem; display: inline-flex; align-items: center; gap: 6px; }
  .note-box { background: #fff; border: 1px solid #dee2e6; border-left: 3px solid #0d6efd; border-radius: 8px; padding: 12px 16px; font-size: 0.83rem; color: #495057; }
  .warn-box { background: #fff; border: 1px solid #dee2e6; border-left: 3px solid #ffc107; border-radius: 8px; padding: 12px 16px; font-size: 0.83rem; color: #495057; }
  .tree { background: #1a1d23; color: #8892a4; border-radius: 8px; padding: 18px 20px; font-family: monospace; font-size: 0.8rem; line-height: 1.8; overflow-x: auto; }
  .tree .dir  { color: #25d07a; }
  .tree .file { color: #e8ecf4; }
  .tree .com  { color: #5a6070; }
  .sidebar { position: sticky; top: 24px; }
  @media (max-width: 991px) { .sidebar { display: none; } }
</style>
</head>
<body>

<!-- HERO -->
<div class="hero">
  <div class="container">
    <div class="d-flex align-items-center gap-3 mb-3">
      <div style="width:48px;height:48px;background:rgba(25,135,84,0.2);border:1px solid rgba(25,135,84,0.3);border-radius:10px;display:grid;place-items:center;color:#25d07a;font-size:1.4rem;">
        <i class="bi bi-camera-video-fill"></i>
      </div>
      <div>
        <h1 class="mb-0 fw-bold" style="font-size:1.9rem;letter-spacing:-0.5px;">ParkVision</h1>
        <p class="subtitle mb-0">Sistema de control de estacionamientos con LPR</p>
      </div>
    </div>
    <div class="d-flex flex-wrap gap-2 mt-3">
      <span class="badge-tech"><i class="bi bi-box me-1"></i>Flask 3.x</span>
      <span class="badge-tech"><i class="bi bi-database me-1"></i>SQLite / SQLAlchemy</span>
      <span class="badge-tech"><i class="bi bi-camera me-1"></i>OpenCV</span>
      <span class="badge-tech"><i class="bi bi-broadcast me-1"></i>SSE</span>
      <span class="badge-tech"><i class="bi bi-bootstrap me-1"></i>Bootstrap 5</span>
      <span class="badge-tech">Python 3.10+</span>
    </div>
  </div>
</div>

<!-- BODY -->
<div class="container py-5">
  <div class="row g-4">

    <!-- SIDEBAR TOC -->
    <div class="col-lg-2">
      <div class="sidebar">
        <div class="section-title mb-2">Contenido</div>
        <nav>
          <a class="toc-link" href="#caracteristicas">Caracteristicas</a>
          <a class="toc-link" href="#arquitectura">Arquitectura</a>
          <a class="toc-link" href="#requisitos">Requisitos</a>
          <a class="toc-link" href="#instalacion">Instalacion</a>
          <a class="toc-link" href="#configuracion">Configuracion</a>
          <a class="toc-link" href="#uso">Uso</a>
          <a class="toc-link" href="#api">API Reference</a>
          <a class="toc-link" href="#estructura">Estructura</a>
          <a class="toc-link" href="#tecnologias">Tecnologias</a>
          <a class="toc-link" href="#notas">Notas</a>
        </nav>
      </div>
    </div>

    <!-- MAIN -->
    <div class="col-lg-10">

      <!-- CARACTERISTICAS -->
      <section id="caracteristicas" class="mb-5">
        <div class="section-title">Caracteristicas</div>
        <div class="row g-3">
          <div class="col-md-6">
            <div class="feature-card d-flex gap-3">
              <div class="icon"><i class="bi bi-camera-video"></i></div>
              <div>
                <h6>Camara Live</h6>
                <p>Deteccion de movimiento por MOG2. Soporte para webcam del navegador, webcam del servidor y camaras IP/RTSP.</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="feature-card d-flex gap-3">
              <div class="icon"><i class="bi bi-upc-scan"></i></div>
              <div>
                <h6>Reconocimiento de Matriculas</h6>
                <p>Integracion con PlateRecognizer API. Modo simulacion automatico cuando no hay API key configurada.</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="feature-card d-flex gap-3">
              <div class="icon"><i class="bi bi-grid-1x2"></i></div>
              <div>
                <h6>Dashboard en Tiempo Real</h6>
                <p>Estadisticas de ocupacion, donut chart y feed de eventos via Server-Sent Events.</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="feature-card d-flex gap-3">
              <div class="icon"><i class="bi bi-people"></i></div>
              <div>
                <h6>Gestion de Vehiculos</h6>
                <p>CRUD completo con soporte para marcar vehiculos como autorizados o bloqueados.</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="feature-card d-flex gap-3">
              <div class="icon"><i class="bi bi-grid-3x3"></i></div>
              <div>
                <h6>Control de Espacios</h6>
                <p>30 espacios en 2 niveles (A y B) con asignacion y liberacion automatica.</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="feature-card d-flex gap-3">
              <div class="icon"><i class="bi bi-clock-history"></i></div>
              <div>
                <h6>Historial de Accesos</h6>
                <p>Registro completo de entradas y salidas con nivel de confianza del reconocimiento y fuente.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ARQUITECTURA -->
      <section id="arquitectura" class="mb-5">
        <div class="section-title">Arquitectura</div>
        <div class="tree mb-3">
<span class="dir">ParkVision/</span>
├── <span class="dir">app/</span>
│   ├── <span class="dir">api/</span>            <span class="com"># Blueprints REST (Flask)</span>
│   │   ├── <span class="file">camera.py</span>   <span class="com"># Stream MJPEG, SSE events, captura</span>
│   │   ├── <span class="file">dashboard.py</span>
│   │   ├── <span class="file">records.py</span>  <span class="com"># Upload de imagenes, registro manual</span>
│   │   ├── <span class="file">slots.py</span>
│   │   └── <span class="file">vehicles.py</span>
│   ├── <span class="dir">models/</span>         <span class="com"># SQLAlchemy ORM</span>
│   └── <span class="dir">services/</span>
│       ├── <span class="file">camera.py</span>         <span class="com"># Captura OpenCV, deteccion de movimiento</span>
│       ├── <span class="file">parking.py</span>        <span class="com"># Logica entrada/salida</span>
│       └── <span class="file">plate_recognizer.py</span>  <span class="com"># API + simulador</span>
├── <span class="dir">static/</span>
├── <span class="dir">templates/</span>
├── <span class="file">run.py</span>
└── <span class="file">requirements.txt</span>
        </div>
        <div class="note-box">
          <strong>Flujo de deteccion automatica:</strong><br>
          Camara &rarr; Deteccion de Movimiento (MOG2 / JS) &rarr; Captura de Frame &rarr; PlateRecognizer API (o simulador) &rarr; <code>process_plate()</code> &rarr; Asignar/liberar espacio &rarr; SSE push &rarr; Dashboard
        </div>
      </section>

      <!-- REQUISITOS -->
      <section id="requisitos" class="mb-5">
        <div class="section-title">Requisitos</div>
        <div class="bg-white border rounded-3 p-3">
          <ul class="mb-0" style="font-size:0.88rem;">
            <li>Python 3.10+</li>
            <li>pip</li>
            <li><span class="text-muted">(Opcional)</span> OpenCV — para modo webcam/IP del servidor</li>
            <li><span class="text-muted">(Opcional)</span> API Key de <a href="https://app.platerecognizer.com/accounts/plan/" target="_blank">PlateRecognizer</a> para reconocimiento real</li>
          </ul>
        </div>
      </section>

      <!-- INSTALACION -->
      <section id="instalacion" class="mb-5">
        <div class="section-title">Instalacion</div>
        <div class="d-flex flex-column gap-3">

          <div class="step-block">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="step-num">1</div>
              <strong style="font-size:0.9rem;">Clonar el repositorio</strong>
            </div>
            <pre>git clone https://github.com/tu-usuario/parkvision.git
cd parkvision</pre>
          </div>

          <div class="step-block">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="step-num">2</div>
              <strong style="font-size:0.9rem;">Crear entorno virtual</strong>
            </div>
            <pre><span class="c"># Linux / macOS</span>
python -m venv venv
source venv/bin/activate

<span class="c"># Windows</span>
python -m venv venv
venv\Scripts\activate</pre>
          </div>

          <div class="step-block">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="step-num">3</div>
              <strong style="font-size:0.9rem;">Instalar dependencias</strong>
            </div>
            <pre>pip install -r requirements.txt</pre>
          </div>

          <div class="step-block">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="step-num">4</div>
              <strong style="font-size:0.9rem;">Configurar variables de entorno</strong>
            </div>
            <p class="text-muted mb-2" style="font-size:0.83rem;">Crea un archivo <code>.env</code> en la raiz del proyecto:</p>
            <div class="env-block">
<span class="key">SECRET_KEY</span>=<span class="val">tu_clave_secreta_aqui</span>
<span class="key">DATABASE_URL</span>=<span class="val">sqlite:///parkvision.db</span>
<span class="key">PLATE_RECOGNIZER_API_KEY</span>=<span class="val">tu_api_key_aqui</span>
<span class="key">CAMERA_COOLDOWN</span>=<span class="val">8</span>
<span class="key">FLASK_DEBUG</span>=<span class="val">false</span>
<span class="key">PORT</span>=<span class="val">5000</span>
            </div>
            <div class="note-box mt-2">
              Si no tienes API key de PlateRecognizer, el sistema funciona en <strong>modo demo</strong> generando matriculas simuladas automaticamente.
            </div>
          </div>

          <div class="step-block">
            <div class="d-flex align-items-center gap-3 mb-2">
              <div class="step-num">5</div>
              <strong style="font-size:0.9rem;">Ejecutar</strong>
            </div>
            <pre>python run.py</pre>
            <p class="mb-0 mt-2 text-muted" style="font-size:0.83rem;">Abre tu navegador en: <code>http://localhost:5000</code></p>
          </div>
        </div>
      </section>

      <!-- CONFIGURACION -->
      <section id="configuracion" class="mb-5">
        <div class="section-title">Configuracion</div>
        <div class="table-responsive">
          <table class="table table-bordered table-hover bg-white" style="font-size:0.83rem;">
            <thead class="table-dark">
              <tr>
                <th>Variable</th>
                <th>Descripcion</th>
                <th>Valor por defecto</th>
              </tr>
            </thead>
            <tbody>
              <tr><td><code>SECRET_KEY</code></td><td>Clave secreta Flask</td><td><code>dev-secret</code></td></tr>
              <tr><td><code>DATABASE_URL</code></td><td>URI de base de datos</td><td><code>sqlite:///parkvision.db</code></td></tr>
              <tr><td><code>PLATE_RECOGNIZER_API_KEY</code></td><td>API key de PlateRecognizer</td><td><code>""</code> (modo simulacion)</td></tr>
              <tr><td><code>CAMERA_COOLDOWN</code></td><td>Segundos entre capturas automaticas</td><td><code>8</code></td></tr>
              <tr><td><code>FLASK_DEBUG</code></td><td>Modo debug</td><td><code>false</code></td></tr>
              <tr><td><code>PORT</code></td><td>Puerto del servidor</td><td><code>5000</code></td></tr>
            </tbody>
          </table>
        </div>

        <p class="fw-semibold mb-2" style="font-size:0.88rem;">Produccion con Gunicorn</p>
        <pre>gunicorn run:app --workers 1 --threads 4 --bind 0.0.0.0:5000</pre>
        <div class="warn-box">
          <i class="bi bi-exclamation-triangle me-1"></i>
          Usar <code>--workers 1</code> porque la camara mantiene estado en memoria (singleton de hilo).
        </div>
      </section>

      <!-- USO -->
      <section id="uso" class="mb-5">
        <div class="section-title">Uso</div>
        <div class="row g-3">
          <div class="col-md-6">
            <div class="bg-white border rounded-3 p-3 h-100">
              <p class="fw-semibold mb-1" style="font-size:0.88rem;"><i class="bi bi-grid-1x2 me-1 text-success"></i> Dashboard</p>
              <p class="text-muted mb-0" style="font-size:0.82rem;">Vista principal con estadisticas de ocupacion en tiempo real, grafico donut y feed de los ultimos eventos.</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="bg-white border rounded-3 p-3 h-100">
              <p class="fw-semibold mb-1" style="font-size:0.88rem;"><i class="bi bi-camera-video me-1 text-success"></i> Camara Live</p>
              <p class="text-muted mb-0" style="font-size:0.82rem;">Tres fuentes disponibles: camara del navegador (WebRTC, sin OpenCV), webcam del servidor, y camara IP/RTSP. La deteccion de movimiento activa capturas automaticamente.</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="bg-white border rounded-3 p-3 h-100">
              <p class="fw-semibold mb-1" style="font-size:0.88rem;"><i class="bi bi-upc-scan me-1 text-success"></i> Escaner</p>
              <p class="text-muted mb-0" style="font-size:0.82rem;">Arrastra o sube una imagen de un vehiculo para reconocer la matricula, o ingresala manualmente para registrar una entrada o salida.</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="bg-white border rounded-3 p-3 h-100">
              <p class="fw-semibold mb-1" style="font-size:0.88rem;"><i class="bi bi-grid-3x3 me-1 text-success"></i> Planta del Parqueo</p>
              <p class="text-muted mb-0" style="font-size:0.82rem;">Vista visual de los 30 espacios distribuidos en 2 niveles (A01-A15 y B01-B15) con disponibilidad en tiempo real.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- API REFERENCE -->
      <section id="api" class="mb-5">
        <div class="section-title">API Reference</div>

        <p class="fw-semibold mb-2" style="font-size:0.85rem;">Formato de respuesta</p>
        <div class="row g-2 mb-4">
          <div class="col-md-6"><pre style="margin:0;">{
  "ok": true,
  "data": { ... }
}</pre></div>
          <div class="col-md-6"><pre style="margin:0;">{
  "ok": false,
  "error": "Mensaje de error"
}</pre></div>
        </div>

        <div class="row g-3">
          <!-- Dashboard -->
          <div class="col-12">
            <p class="fw-semibold mb-2" style="font-size:0.85rem; color:#1a1d23;">Dashboard</p>
            <div class="table-responsive">
              <table class="table table-bordered bg-white mb-0" style="font-size:0.82rem;">
                <thead class="table-dark"><tr><th>Metodo</th><th>Endpoint</th><th>Descripcion</th></tr></thead>
                <tbody>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/dashboard/stats</td><td>Estadisticas generales</td></tr>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/dashboard/inside</td><td>Vehiculos actualmente dentro</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Vehiculos -->
          <div class="col-12">
            <p class="fw-semibold mb-2" style="font-size:0.85rem; color:#1a1d23;">Vehiculos</p>
            <div class="table-responsive">
              <table class="table table-bordered bg-white mb-0" style="font-size:0.82rem;">
                <thead class="table-dark"><tr><th>Metodo</th><th>Endpoint</th><th>Descripcion</th></tr></thead>
                <tbody>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/vehicles/</td><td>Listar todos</td></tr>
                  <tr><td><span class="method-badge method-post">POST</span></td><td class="endpoint">/api/vehicles/</td><td>Crear vehiculo</td></tr>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/vehicles/&lt;id&gt;</td><td>Obtener por ID</td></tr>
                  <tr><td><span class="method-badge method-patch">PATCH</span></td><td class="endpoint">/api/vehicles/&lt;id&gt;</td><td>Actualizar</td></tr>
                  <tr><td><span class="method-badge method-delete">DELETE</span></td><td class="endpoint">/api/vehicles/&lt;id&gt;</td><td>Eliminar</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Registros -->
          <div class="col-12">
            <p class="fw-semibold mb-2" style="font-size:0.85rem; color:#1a1d23;">Registros</p>
            <div class="table-responsive">
              <table class="table table-bordered bg-white mb-0" style="font-size:0.82rem;">
                <thead class="table-dark"><tr><th>Metodo</th><th>Endpoint</th><th>Descripcion</th></tr></thead>
                <tbody>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/records/</td><td>Historial (param: ?limit=100)</td></tr>
                  <tr><td><span class="method-badge method-post">POST</span></td><td class="endpoint">/api/records/upload</td><td>Subir imagen para reconocimiento</td></tr>
                  <tr><td><span class="method-badge method-post">POST</span></td><td class="endpoint">/api/records/manual</td><td>Registro manual de matricula</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Camara -->
          <div class="col-12">
            <p class="fw-semibold mb-2" style="font-size:0.85rem; color:#1a1d23;">Camara</p>
            <div class="table-responsive">
              <table class="table table-bordered bg-white mb-0" style="font-size:0.82rem;">
                <thead class="table-dark"><tr><th>Metodo</th><th>Endpoint</th><th>Descripcion</th></tr></thead>
                <tbody>
                  <tr><td><span class="method-badge method-post">POST</span></td><td class="endpoint">/api/camera/start</td><td>Iniciar camara del servidor</td></tr>
                  <tr><td><span class="method-badge method-post">POST</span></td><td class="endpoint">/api/camera/stop</td><td>Detener camara</td></tr>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/camera/status</td><td>Estado actual</td></tr>
                  <tr><td><span class="method-badge method-post">POST</span></td><td class="endpoint">/api/camera/capture</td><td>Captura y reconocimiento manual</td></tr>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/camera/stream</td><td>Stream MJPEG</td></tr>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/camera/events</td><td>SSE — eventos en tiempo real</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <!-- Espacios -->
          <div class="col-12">
            <p class="fw-semibold mb-2" style="font-size:0.85rem; color:#1a1d23;">Espacios</p>
            <div class="table-responsive">
              <table class="table table-bordered bg-white mb-0" style="font-size:0.82rem;">
                <thead class="table-dark"><tr><th>Metodo</th><th>Endpoint</th><th>Descripcion</th></tr></thead>
                <tbody>
                  <tr><td><span class="method-badge method-get">GET</span></td><td class="endpoint">/api/slots/</td><td>Listar todos los espacios</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- ESTRUCTURA -->
      <section id="estructura" class="mb-5">
        <div class="section-title">Estructura del Proyecto</div>
        <div class="tree">
<span class="dir">parkvision/</span>
├── <span class="dir">app/</span>
│   ├── <span class="file">__init__.py</span>           <span class="com"># App factory, seed inicial</span>
│   ├── <span class="dir">api/</span>
│   │   ├── <span class="file">_helpers.py</span>       <span class="com"># success(), error(), validate_json()</span>
│   │   ├── <span class="file">camera.py</span>
│   │   ├── <span class="file">dashboard.py</span>
│   │   ├── <span class="file">records.py</span>
│   │   ├── <span class="file">slots.py</span>
│   │   └── <span class="file">vehicles.py</span>
│   ├── <span class="dir">models/</span>
│   │   ├── <span class="file">record.py</span>         <span class="com"># ParkingRecord</span>
│   │   ├── <span class="file">slot.py</span>           <span class="com"># ParkingSlot (assign/release)</span>
│   │   └── <span class="file">vehicle.py</span>        <span class="com"># Vehicle</span>
│   └── <span class="dir">services/</span>
│       ├── <span class="file">camera.py</span>         <span class="com"># Singleton de camara + MOG2</span>
│       ├── <span class="file">parking.py</span>        <span class="com"># process_plate(), get_stats()</span>
│       └── <span class="file">plate_recognizer.py</span>
├── <span class="dir">instance/</span>
│   └── <span class="file">parkvision.db</span>         <span class="com"># Base de datos SQLite (auto-generada)</span>
├── <span class="dir">static/</span>
│   ├── <span class="dir">css/</span>
│   ├── <span class="dir">js/</span>
│   └── <span class="dir">uploads/</span>              <span class="com"># Imagenes capturadas</span>
├── <span class="dir">templates/</span>
│   └── <span class="file">index.html</span>            <span class="com"># SPA unica pagina</span>
├── <span class="file">.env</span>                      <span class="com"># Variables de entorno (no commitear)</span>
├── <span class="file">.gitignore</span>
├── <span class="file">requirements.txt</span>
└── <span class="file">run.py</span>
        </div>
      </section>

      <!-- TECNOLOGIAS -->
      <section id="tecnologias" class="mb-5">
        <div class="section-title">Tecnologias</div>
        <div class="row g-4">
          <div class="col-md-6">
            <p class="fw-semibold mb-2" style="font-size:0.85rem;">Backend</p>
            <div class="d-flex flex-wrap gap-2">
              <span class="tech-badge"><i class="bi bi-box text-success"></i> Flask 3.x</span>
              <span class="tech-badge"><i class="bi bi-database text-primary"></i> Flask-SQLAlchemy</span>
              <span class="tech-badge">Flask-Migrate</span>
              <span class="tech-badge"><i class="bi bi-camera text-danger"></i> OpenCV</span>
              <span class="tech-badge">Pillow</span>
              <span class="tech-badge">Gunicorn</span>
              <span class="tech-badge">PlateRecognizer API</span>
            </div>
          </div>
          <div class="col-md-6">
            <p class="fw-semibold mb-2" style="font-size:0.85rem;">Frontend</p>
            <div class="d-flex flex-wrap gap-2">
              <span class="tech-badge"><i class="bi bi-bootstrap text-primary"></i> Bootstrap 5.3</span>
              <span class="tech-badge"><i class="bi bi-grid text-primary"></i> Bootstrap Icons</span>
              <span class="tech-badge">Vanilla JS</span>
              <span class="tech-badge">SSE</span>
              <span class="tech-badge">WebRTC</span>
            </div>
          </div>
          <div class="col-md-6">
            <p class="fw-semibold mb-2" style="font-size:0.85rem;">Base de Datos</p>
            <div class="d-flex flex-wrap gap-2">
              <span class="tech-badge"><i class="bi bi-file-earmark-binary text-warning"></i> SQLite (desarrollo)</span>
              <span class="tech-badge text-muted">PostgreSQL / MySQL (produccion)</span>
            </div>
            <p class="text-muted mt-2 mb-0" style="font-size:0.78rem;">Reemplazable via variable <code>DATABASE_URL</code>.</p>
          </div>
        </div>
      </section>

      <!-- NOTAS -->
      <section id="notas" class="mb-5">
        <div class="section-title">Notas</div>
        <div class="bg-white border rounded-3 p-3">
          <ul class="mb-0" style="font-size:0.85rem; line-height:2;">
            <li>La base de datos se crea automaticamente al primer inicio con 30 espacios y 5 vehiculos de ejemplo.</li>
            <li>El modo simulacion genera matriculas aleatorias con formato <code>XXX-000</code> cuando no hay API key configurada.</li>
            <li>Las imagenes capturadas se guardan en <code>static/uploads/</code>.</li>
            <li>Agregar <code>static/uploads/</code> e <code>instance/</code> al <code>.gitignore</code> para no subir datos ni la BD al repositorio.</li>
          </ul>
        </div>
      </section>

    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
  // Highlight active TOC link on scroll
  const sections = document.querySelectorAll('section[id]');
  const links = document.querySelectorAll('.toc-link');
  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(s => { if (window.scrollY >= s.offsetTop - 80) current = s.id; });
    links.forEach(l => {
      l.classList.toggle('active', l.getAttribute('href') === '#' + current);
    });
  });
</script>
</body>
</html>