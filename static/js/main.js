'use strict';

const State = {
  feedEvents:       [],
  camRunning:       false,
  camMode:          'browser',
  browserStream:    null,
  motionTimer:      null,
  serverPollTimer:  null,
  browserCooldownTs: 0,
  sseSource:        null,
  bsToast:          null,
  bsModal:          null,
};

document.addEventListener('DOMContentLoaded', () => {
  State.bsToast = new bootstrap.Toast(document.getElementById('toast'), { delay: 5000 });
  State.bsModal = new bootstrap.Modal(document.getElementById('vehicleModal'));
  setupDropZone();
  setupCamModeSwitch();
  SSE.connect();
  refreshAll();
  setInterval(refreshAll, 15_000);
  setInterval(Clock.tick, 1_000);
  Clock.tick();
});

// ── CLOCK ──────────────────────────────────────────────────────
const Clock = {
  tick() {
    const now = new Date();
    setText('clock', now.toLocaleString('es-PE', {
      weekday: 'long', day: 'numeric', month: 'long',
      hour: '2-digit', minute: '2-digit',
    }));
    const hud = document.getElementById('hud-clock');
    if (hud) hud.textContent = now.toLocaleTimeString('es-PE');
  },
};

// ── NAV ─────────────────────────────────────────────────────────
function nav(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
  document.getElementById(`pg-${page}`).classList.add('active');
  document.querySelector(`[data-page="${page}"]`).classList.add('active');
  ({ inside: loadInside, vehicles: loadVehicles, history: loadHistory, slots: loadSlots })[page]?.();
}

// ── REFRESH ──────────────────────────────────────────────────────
async function refreshAll() {
  await Promise.all([loadStats(), loadInsideCount()]);
}

async function loadStats() {
  const res = await API.get('/api/dashboard/stats');
  if (!res.ok) return;
  const d = res.data;
  setText('s-free',  d.free);
  setText('s-occ',   d.occupied);
  setText('s-today', d.entries_today);
  setText('s-unk',   d.unknown_today);
  Donut.update(d.occupied, d.total_slots);
  setText('leg-occ',  d.occupied);
  setText('leg-free', d.free);
}

async function loadInsideCount() {
  const res = await API.get('/api/dashboard/inside');
  if (!res.ok) return;
  setText('inside-badge', res.data.length);
}

// ── DONUT ────────────────────────────────────────────────────────
const Donut = {
  update(occ, total) {
    if (!total) return;
    const pct  = occ / total;
    const circ = 2 * Math.PI * 55;
    const arc  = document.getElementById('donut-arc');
    if (arc) arc.setAttribute('stroke-dasharray', `${circ * pct} ${circ * (1 - pct)}`);
    setText('donut-pct', `${Math.round(pct * 100)}%`);
  },
};

// ── FEED ─────────────────────────────────────────────────────────
const Feed = {
  push(event) {
    State.feedEvents.unshift(event);
    if (State.feedEvents.length > 30) State.feedEvents.pop();
    this.render();
  },
  render() {
    const el = document.getElementById('dash-feed');
    if (!el) return;
    if (!State.feedEvents.length) {
      el.innerHTML = '<p class="text-center text-muted py-4 mb-0">Sin eventos aun</p>';
      return;
    }
    const cls  = e => e.vehicle?.authorized === false ? 'fi-red'   : e.event_type === 'exit' ? 'fi-blue'  : e.is_known ? 'fi-green' : 'fi-amber';
    const tag  = e => e.vehicle?.authorized === false ? 'danger'   : e.event_type === 'exit' ? 'primary'  : e.is_known ? 'success'  : 'warning';
    const lbl  = e => e.vehicle?.authorized === false ? 'BLOQUEADO': e.event_type === 'exit' ? 'Salida'   : e.is_known ? 'Conocido' : 'Desconocido';
    el.innerHTML = State.feedEvents.slice(0, 12).map(e => `
      <div class="feed-item ${cls(e)}">
        <div class="flex-grow-1">
          <div class="fi-plate">${e.plate}</div>
          <div class="fi-owner">${e.vehicle?.owner_name ?? 'Sin registro'}</div>
        </div>
        <span class="badge bg-${tag(e)}">${lbl(e)}</span>
        <span class="fi-time">${fmtTime(e.timestamp ?? new Date().toISOString())}</span>
      </div>`).join('');
  },
};

// ── SSE ──────────────────────────────────────────────────────────
const SSE = {
  connect() {
    if (State.sseSource) State.sseSource.close();
    State.sseSource = new EventSource('/api/camera/events');
    State.sseSource.onmessage = e => {
      try {
        const ev = JSON.parse(e.data);
        Feed.push(ev);
        Toast.show(ev);
        Detections.add(ev);
        refreshAll();
      } catch (_) {}
    };
    State.sseSource.onerror = () => setTimeout(() => SSE.connect(), 5_000);
  },
};

// ── TOAST ────────────────────────────────────────────────────────
const Toast = {
  show(event) {
    const isKnown = event.is_known;
    const isExit  = event.event_type === 'exit';
    setText('toast-plate', event.plate);
    document.getElementById('toast-info').textContent = [
      event.vehicle?.owner_name ?? 'Desconocido',
      isExit ? 'Salida' : 'Entrada',
      event.slot_code ? `· Espacio ${event.slot_code}` : '',
    ].filter(Boolean).join(' · ');
    document.getElementById('toast-time').textContent = new Date().toLocaleTimeString('es-PE');
    State.bsToast.show();
  },
};

// ── TABLES ───────────────────────────────────────────────────────
async function loadInside() {
  const res = await API.get('/api/dashboard/inside');
  if (!res.ok) return;
  const tbody = document.getElementById('inside-tbody');
  if (!res.data.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-4">No hay vehiculos dentro</td></tr>';
    return;
  }
  tbody.innerHTML = res.data.map(r => `<tr>
    <td><code>${r.plate}</code></td>
    <td>${r.vehicle?.owner_name ?? '—'}</td>
    <td><code class="text-primary">${r.slot_code ?? '—'}</code></td>
    <td>${fmtDateTime(r.entry_time)}</td>
    <td>${r.duration_minutes} min</td>
    <td><span class="badge bg-${r.is_known ? 'success' : 'warning'}">${r.is_known ? 'Conocido' : 'Desconocido'}</span></td>
  </tr>`).join('');
}

async function loadVehicles() {
  const res = await API.get('/api/vehicles/');
  if (!res.ok) return;
  const tbody = document.getElementById('vehicles-tbody');
  if (!res.data.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-4">No hay vehiculos registrados</td></tr>';
    return;
  }
  tbody.innerHTML = res.data.map(v => `<tr>
    <td><code>${v.plate}</code></td>
    <td>${v.owner_name ?? '—'}</td>
    <td>${[v.brand, v.model].filter(Boolean).join(' ') || '—'}</td>
    <td>${v.color ?? '—'}</td>
    <td>${v.year ?? '—'}</td>
    <td><span class="badge bg-${v.authorized ? 'success' : 'danger'}">${v.authorized ? 'Autorizado' : 'Bloqueado'}</span></td>
    <td><button class="btn btn-outline-danger btn-sm" onclick="deleteVehicle(${v.id})">
      <i class="bi bi-trash"></i>
    </button></td>
  </tr>`).join('');
}

async function loadHistory() {
  const res = await API.get('/api/records/?limit=100');
  if (!res.ok) return;
  const tbody = document.getElementById('history-tbody');
  if (!res.data.length) {
    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4">Sin registros aun</td></tr>';
    return;
  }
  tbody.innerHTML = res.data.map(r => {
    const pct = Math.round((r.confidence ?? 0) * 100);
    return `<tr>
      <td><code>${r.plate}</code></td>
      <td>${r.owner_name ?? '—'}</td>
      <td><span class="badge bg-${r.event_type === 'entry' ? 'success' : 'primary'}">${r.event_type === 'entry' ? 'Entrada' : 'Salida'}</span></td>
      <td>${fmtDateTime(r.entry_time)}</td>
      <td>${r.exit_time ? fmtDateTime(r.exit_time) : '<span class="badge bg-success">Dentro</span>'}</td>
      <td><code class="text-primary">${r.slot_code ?? '—'}</code></td>
      <td>
        <div class="d-flex align-items-center gap-2">
          <small class="text-muted font-monospace">${pct}%</small>
          <div class="progress flex-grow-1" style="height:4px;width:60px">
            <div class="progress-bar bg-success" style="width:${pct}%"></div>
          </div>
        </div>
      </td>
      <td><span class="badge bg-secondary">${r.source}</span></td>
    </tr>`;
  }).join('');
}

async function loadSlots() {
  const res = await API.get('/api/slots/');
  if (!res.ok) return;
  ['A', 'B'].forEach(l => document.getElementById(`slots-${l}`).innerHTML = '');
  res.data.forEach(s => {
    const div = document.createElement('div');
    div.className = `slot ${s.occupied ? 'sl-occ' : 'sl-free'}`;
    div.innerHTML = `<span class="fw-bold">${s.code}</span>${s.occupied ? `<span class="slot-plate">${s.plate ?? ''}</span>` : ''}`;
    document.getElementById(`slots-${s.level === 1 ? 'A' : 'B'}`).appendChild(div);
  });
}

// ── VEHICLES CRUD ─────────────────────────────────────────────────
function openVehicleModal() { State.bsModal.show(); }

async function saveVehicle() {
  const plate = document.getElementById('f-plate').value.trim().toUpperCase();
  if (!plate) { alert('La matricula es obligatoria'); return; }
  const res = await API.post('/api/vehicles/', {
    plate,
    owner_name:   document.getElementById('f-name').value,
    owner_doc:    document.getElementById('f-doc').value,
    brand:        document.getElementById('f-brand').value,
    model:        document.getElementById('f-model').value,
    color:        document.getElementById('f-color').value,
    year:         parseInt(document.getElementById('f-year').value) || null,
    vehicle_type: document.getElementById('f-type').value,
    notes:        document.getElementById('f-notes').value,
    authorized:   true,
  });
  if (res.ok) { State.bsModal.hide(); loadVehicles(); refreshAll(); }
  else alert(res.error ?? 'Error al guardar');
}

async function deleteVehicle(id) {
  if (!confirm('Eliminar este vehiculo?')) return;
  await API.del(`/api/vehicles/${id}`);
  loadVehicles(); refreshAll();
}

// ── SCANNER ──────────────────────────────────────────────────────
function setupDropZone() {
  const zone = document.getElementById('drop-zone');
  const inp  = document.getElementById('file-in');
  if (!zone) return;
  zone.addEventListener('click', () => inp.click());
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag'));
  zone.addEventListener('drop', e => { e.preventDefault(); zone.classList.remove('drag'); if (e.dataTransfer.files[0]) setPreview(e.dataTransfer.files[0]); });
  inp.addEventListener('change', () => { if (inp.files[0]) setPreview(inp.files[0]); });
}

function setPreview(file) {
  const reader = new FileReader();
  reader.onload = e => {
    const img = document.getElementById('preview-img');
    img.src = e.target.result; img.style.display = 'block';
    document.getElementById('drop-content').style.display = 'none';
    document.getElementById('btn-scan').disabled = false;
  };
  reader.readAsDataURL(file);
}

async function scanUpload() {
  const file = document.getElementById('file-in').files[0];
  if (!file) return;
  const btn = document.getElementById('btn-scan');
  btn.disabled = true; btn.textContent = 'Analizando...';
  const form = new FormData();
  form.append('image', file);
  try {
    const resp = await fetch('/api/records/upload', { method: 'POST', body: form });
    const json = await resp.json();
    if (resp.ok) { renderResult(json.data); Feed.push(json.data); Toast.show(json.data); refreshAll(); }
    else renderResultError(json.error ?? 'No se detecto placa');
  } catch { renderResultError('Error de conexion'); }
  btn.disabled = false; btn.innerHTML = '<i class="bi bi-upc-scan"></i> Reconocer Matricula';
}

async function manualEntry() {
  const plate = document.getElementById('manual-plate').value.trim();
  if (!plate) return;
  const res = await API.post('/api/records/manual', { plate });
  if (res.ok) { renderResult(res.data); Feed.push(res.data); Toast.show(res.data); refreshAll(); }
  else renderResultError(res.error ?? 'Error');
}

function renderResult(event) {
  const isEntry   = event.event_type === 'entry';
  const isKnown   = event.is_known;
  const isBlocked = event.vehicle?.authorized === false;
  const v         = event.vehicle ?? {};
  const pct       = Math.round((event.confidence ?? 0) * 100);
  const plateColor = isBlocked ? 'danger' : isKnown ? 'success' : 'warning';

  let alertHtml = '';
  if (isBlocked)     alertHtml = `<div class="alert alert-danger mt-3 py-2 small mb-0">Acceso denegado — vehiculo bloqueado</div>`;
  else if (!isKnown) alertHtml = `<div class="alert alert-warning mt-3 py-2 small mb-0">Vehiculo no registrado — requiere atencion</div>`;
  else if (!isEntry) alertHtml = `<div class="alert alert-info mt-3 py-2 small mb-0">Salida registrada${event.slot_code ? ` · Espacio ${event.slot_code}` : ''}</div>`;
  else               alertHtml = `<div class="alert alert-success mt-3 py-2 small mb-0">Acceso permitido${event.slot_code ? ` · Espacio asignado: <strong>${event.slot_code}</strong>` : ''}</div>`;

  document.getElementById('result-panel').innerHTML = `
    <div class="w-100">
      <div class="d-flex align-items-center gap-3 mb-3 flex-wrap">
        <span class="badge bg-${plateColor} font-monospace fs-5 px-3 py-2 letter-spacing-wide">${event.plate}</span>
        <span class="badge bg-${isEntry ? (isKnown ? 'success' : 'warning') : 'primary'}">${isEntry ? (isKnown ? 'Conocido' : 'Desconocido') : 'Salida'}</span>
        ${event.simulated ? '<span class="badge bg-secondary">DEMO</span>' : ''}
      </div>
      <table class="table table-sm table-bordered mb-0">
        <tr><td class="text-muted small">Propietario</td><td class="font-monospace small">${v.owner_name ?? 'No registrado'}</td></tr>
        <tr><td class="text-muted small">Vehiculo</td><td class="font-monospace small">${[v.brand, v.model].filter(Boolean).join(' ') || '—'}</td></tr>
        <tr><td class="text-muted small">Color / Año</td><td class="font-monospace small">${[v.color, v.year].filter(Boolean).join(' · ') || '—'}</td></tr>
        <tr><td class="text-muted small">Evento</td><td class="font-monospace small"><strong class="text-${isEntry ? 'success' : 'primary'}">${isEntry ? 'ENTRADA' : 'SALIDA'}</strong></td></tr>
        <tr><td class="text-muted small">Confianza</td><td>
          <div class="d-flex align-items-center gap-2">
            <small class="font-monospace">${pct}%</small>
            <div class="progress flex-grow-1" style="height:5px"><div class="progress-bar bg-success" style="width:${pct}%"></div></div>
          </div>
        </td></tr>
      </table>
      ${alertHtml}
    </div>`;
  document.getElementById('result-panel').style.alignItems = 'flex-start';
}

function renderResultError(msg) {
  document.getElementById('result-panel').innerHTML =
    `<div class="alert alert-danger mb-0">${msg}</div>`;
}

// ── CAMERA ───────────────────────────────────────────────────────
function setupCamModeSwitch() {
  document.getElementById('cam-mode')?.addEventListener('change', onCamModeChange);
}
function onCamModeChange() {
  const mode = document.getElementById('cam-mode').value;
  document.getElementById('cfg-index').style.display = mode === 'webcam' ? '' : 'none';
  document.getElementById('cfg-url').style.display   = mode === 'ip'     ? '' : 'none';
}
async function toggleCam() { State.camRunning ? await stopCam() : await startCam(); }

async function startCam() {
  State.camMode = document.getElementById('cam-mode').value;
  const btn = document.getElementById('btn-cam');
  btn.disabled = true; btn.textContent = 'Conectando...';
  try {
    State.camMode === 'browser' ? await startBrowserCam() : await startServerCam();
    State.camRunning = true;
    updateCamUI(true);
    document.getElementById('btn-capture').disabled = false;
  } catch (err) { alert(`Error al iniciar camara: ${err.message}`); }
  btn.disabled = false;
}

async function stopCam() {
  if (State.browserStream) { State.browserStream.getTracks().forEach(t => t.stop()); State.browserStream = null; }
  clearInterval(State.motionTimer);
  clearInterval(State.serverPollTimer);
  if (State.camMode !== 'browser') {
    await API.post('/api/camera/stop', {});
    document.getElementById('cam-mjpeg').style.display = 'none';
    document.getElementById('cam-mjpeg').src = '';
  } else {
    document.getElementById('cam-video').style.display = 'none';
  }
  document.getElementById('cam-hud').style.display        = 'none';
  document.getElementById('cam-placeholder').style.display = 'flex';
  document.getElementById('btn-capture').disabled = true;
  State.camRunning = false;
  updateCamUI(false);
}

async function startServerCam() {
  const index = parseInt(document.getElementById('cam-index').value) || 0;
  const url   = document.getElementById('cam-url').value.trim();
  const res   = await API.post('/api/camera/start', { mode: State.camMode, index, url });
  if (!res.ok) throw new Error(res.error ?? 'Error al iniciar');
  await sleep(800);
  const img = document.getElementById('cam-mjpeg');
  img.src = `/api/camera/stream?t=${Date.now()}`;
  img.style.display = 'block';
  document.getElementById('cam-placeholder').style.display = 'none';
  document.getElementById('cam-hud').style.display         = 'block';
  State.serverPollTimer = setInterval(async () => {
    const s = await API.get('/api/camera/status');
    if (!s.ok) return;
    setText('chip-fps', `FPS ${s.data.fps}`);
    setText('chip-res', s.data.resolution);
    updateMotionChip(s.data.motion);
  }, 2_000);
}

async function startBrowserCam() {
  try {
    State.browserStream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false,
    });
  } catch (err) {
    const msgs = {
      NotAllowedError:   'Permiso de camara denegado. Acepta el permiso en el navegador.',
      NotFoundError:     'No se encontro ninguna camara conectada.',
      NotReadableError:  'La camara esta siendo usada por otra aplicacion.',
    };
    throw new Error(msgs[err.name] ?? `${err.name}: ${err.message}`);
  }
  const video = document.getElementById('cam-video');
  video.srcObject = State.browserStream; video.style.display = 'block';
  document.getElementById('cam-placeholder').style.display = 'none';
  document.getElementById('cam-hud').style.display         = 'block';
  setText('chip-fps', 'FPS ~30'); setText('chip-res', '1280x720');
  let prevData = null;
  State.motionTimer = setInterval(() => {
    prevData = detectMotion(video, prevData, (motion, newData) => {
      prevData = newData;
      updateMotionChip(motion);
      document.getElementById('hud-roi')?.classList.toggle('motion', motion);
      const lbl = document.getElementById('hud-motion');
      if (lbl) { lbl.textContent = motion ? 'MOVIMIENTO' : 'EN VIVO'; lbl.classList.toggle('motion', motion); }
      const cooldown = parseInt(document.getElementById('cooldown').value) || 8;
      if (motion && document.getElementById('auto-tog').checked &&
          (Date.now() - State.browserCooldownTs) > cooldown * 1_000) {
        State.browserCooldownTs = Date.now();
        captureNow();
      }
    });
  }, 500);
}

function detectMotion(video, prev, cb) {
  if (video.readyState < 2) { cb(false, prev); return prev; }
  const canvas = document.getElementById('cam-canvas');
  const W = 160, H = 90;
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, W, H);
  const curr = ctx.getImageData(0, 0, W, H);
  if (!prev) { cb(false, curr); return curr; }
  let diff = 0;
  for (let i = 0; i < curr.data.length; i += 4) {
    diff += Math.abs(curr.data[i]   - prev.data[i])
          + Math.abs(curr.data[i+1] - prev.data[i+1])
          + Math.abs(curr.data[i+2] - prev.data[i+2]);
  }
  cb(diff > 800_000, curr);
  return curr;
}

function updateMotionChip(motion) {
  const chip = document.getElementById('chip-motion');
  if (!chip) return;
  chip.textContent = motion ? 'MOVIMIENTO' : 'SIN MOVIMIENTO';
  chip.className   = `badge ${motion ? 'bg-danger' : 'bg-secondary'}`;
}

async function captureNow() {
  document.getElementById('btn-capture').disabled = true;
  let body = {};
  if (State.camMode === 'browser') {
    const video = document.getElementById('cam-video');
    const canvas = document.getElementById('cam-canvas');
    canvas.width = video.videoWidth || 1280; canvas.height = video.videoHeight || 720;
    canvas.getContext('2d').drawImage(video, 0, 0);
    body = { frame_b64: canvas.toDataURL('image/jpeg', 0.9) };
  }
  const res = await API.post('/api/camera/capture', body);
  if (res.ok) { Detections.add(res.data); Feed.push(res.data); Toast.show(res.data); refreshAll(); }
  document.getElementById('btn-capture').disabled = false;
}

function updateCamUI(running) {
  const btn  = document.getElementById('btn-cam');
  const badge = document.getElementById('cam-badge');
  const pill  = document.getElementById('cam-status-pill');
  const dot   = document.getElementById('status-dot');
  if (running) {
    btn.innerHTML = '<i class="bi bi-stop-fill"></i> Detener';
    btn.className = 'btn btn-danger btn-sm';
    badge.textContent = 'ON'; badge.className = 'badge bg-success ms-auto';
    pill.textContent = State.camMode === 'browser' ? 'Camara navegador' : 'Webcam activa';
    pill.className = 'badge rounded-pill live';
    dot.classList.add('live');
    document.getElementById('status-txt').textContent = 'Camara activa';
  } else {
    btn.innerHTML = '<i class="bi bi-play-fill"></i> Iniciar Camara';
    btn.className = 'btn btn-success btn-sm';
    badge.textContent = 'OFF'; badge.className = 'badge bg-secondary ms-auto';
    pill.textContent = 'Desconectada'; pill.className = 'badge rounded-pill';
    dot.classList.remove('live');
    document.getElementById('status-txt').textContent = 'Modo Demo';
    setText('chip-fps', 'FPS —'); setText('chip-res', '— x —');
    updateMotionChip(false);
  }
}

// ── DETECTIONS ────────────────────────────────────────────────────
const Detections = {
  add(event) {
    const list = document.getElementById('det-list');
    if (!list) return;
    list.querySelector('p')?.remove();
    const isExit    = event.event_type === 'exit';
    const isKnown   = event.is_known;
    const isBlocked = event.vehicle?.authorized === false;
    const cls  = isBlocked ? 'dc-red'   : isExit ? 'dc-blue'  : isKnown ? 'dc-green' : 'dc-amber';
    const tag  = isBlocked ? 'danger'   : isExit ? 'primary'  : isKnown ? 'success'  : 'warning';
    const lbl  = isBlocked ? 'Bloqueado': isExit ? 'Salida'   : isKnown ? 'Conocido' : 'Desconocido';
    const pct  = Math.round((event.confidence ?? 0) * 100);
    const card = document.createElement('div');
    card.className = `det-card ${cls}`;
    card.innerHTML = `
      <div class="det-plate">${event.plate}</div>
      <div class="det-meta">
        <span>${event.vehicle?.owner_name ?? 'Sin registro'}</span>
        <span>${new Date().toLocaleTimeString('es-PE')}</span>
      </div>
      <div class="det-tags">
        <span class="badge bg-${tag}">${lbl}</span>
        ${event.slot_code ? `<span class="badge bg-primary">${event.slot_code}</span>` : ''}
        ${event.source === 'camera' ? `<span class="badge bg-secondary">Auto</span>` : ''}
        <span class="badge bg-light text-dark">${pct}%</span>
      </div>`;
    list.insertBefore(card, list.firstChild);
    while (list.children.length > 40) list.removeChild(list.lastChild);
  },
};

function clearDets() {
  const list = document.getElementById('det-list');
  if (list) list.innerHTML = '<p class="text-center text-muted small py-4 mb-0">Lista limpiada</p>';
}

// ── API ──────────────────────────────────────────────────────────
const API = {
  async get(url) {
    try {
      const r = await fetch(url);
      const j = await r.json();
      return r.ok ? j : { ok: false, error: j.error ?? 'Error' };
    } catch { return { ok: false, error: 'Network error' }; }
  },
  async post(url, body) {
    try {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const j = await r.json();
      return r.ok ? j : { ok: false, error: j.error ?? 'Error' };
    } catch { return { ok: false, error: 'Network error' }; }
  },
  async del(url) {
    try { return await (await fetch(url, { method: 'DELETE' })).json(); }
    catch { return { ok: false }; }
  },
};

// ── UTILS ─────────────────────────────────────────────────────────
function setText(id, val) { const el = document.getElementById(id); if (el) el.textContent = val; }
function fmtDateTime(iso) { if (!iso) return '—'; return new Date(iso).toLocaleString('es-PE', { day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit' }); }
function fmtTime(iso)     { if (!iso) return '—'; return new Date(iso).toLocaleTimeString('es-PE', { hour:'2-digit', minute:'2-digit' }); }
function sleep(ms)        { return new Promise(r => setTimeout(r, ms)); }