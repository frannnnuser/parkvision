import os
import threading
import time
from datetime import datetime
from dataclasses import dataclass, field

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

SNAPSHOT_DIR = "static/uploads"


@dataclass
class _State:
    running:      bool  = False
    motion:       bool  = False
    fps:          float = 0.0
    width:        int   = 0
    height:       int   = 0
    mode:         str   = "webcam"
    last_capture: float = 0.0
    _lock:        threading.Lock = field(default_factory=threading.Lock)
    _frame:       bytes = None

    def write(self, jpg):
        with self._lock:
            self._frame = jpg

    def read(self):
        with self._lock:
            return self._frame


_state        = _State()
_on_motion_cb = None
_cooldown     = 8


def start(mode="webcam", index=0, url="", cooldown=8, on_motion=None):
    global _on_motion_cb, _cooldown
    if _state.running:
        return False, "Camera already running"
    if mode in ("webcam", "ip") and not CV2_AVAILABLE:
        return False, "OpenCV not installed"
    _on_motion_cb   = on_motion
    _cooldown       = cooldown
    _state.mode     = mode
    _state.running  = True
    _state.last_capture = 0.0
    threading.Thread(target=_loop, args=(index, url), daemon=True).start()
    return True, "Camera started"


def stop():
    _state.running = False
    return True, "Camera stopped"


def get_frame():
    return _state.read()


def get_status():
    return {
        "running":    _state.running,
        "motion":     _state.motion,
        "fps":        _state.fps,
        "resolution": f"{_state.width}x{_state.height}",
        "mode":       _state.mode,
    }


def capture_frame():
    jpg = _state.read()
    if not jpg:
        return None
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(SNAPSHOT_DIR, f"snap_{ts}.jpg")
    with open(path, "wb") as f:
        f.write(jpg)
    return path


def save_b64_frame(b64: str):
    import base64
    import io
    try:
        from PIL import Image
        data = base64.b64decode(b64.split(",")[-1])
        img  = Image.open(io.BytesIO(data))
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = os.path.join(SNAPSHOT_DIR, f"browser_{ts}.jpg")
        img.save(path, quality=90)
        return path
    except Exception:
        return None


def _loop(index, url):
    source = url if _state.mode == "ip" else index
    cap    = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        _state.running = False
        return

    _state.width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    _state.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fgbg        = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=40)
    kernel      = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    frame_count = 0
    fps_ts      = time.monotonic()

    while _state.running:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.1)
            continue

        frame_count += 1
        small  = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
        mask   = fgbg.apply(small)
        mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        motion = int(cv2.countNonZero(mask)) > 3000
        _state.motion = motion

        now = time.monotonic()
        if motion and _on_motion_cb and (now - _state.last_capture) > _cooldown:
            _state.last_capture = now
            _fire_detection(frame.copy())

        display      = _overlay(frame, motion)
        ok2, buf     = cv2.imencode(".jpg", display, [cv2.IMWRITE_JPEG_QUALITY, 72])
        if ok2:
            _state.write(buf.tobytes())

        elapsed = time.monotonic() - fps_ts
        if elapsed >= 2.0:
            _state.fps  = round(frame_count / elapsed, 1)
            frame_count = 0
            fps_ts      = time.monotonic()

        time.sleep(0.030)

    cap.release()
    _state.write(None)


def _fire_detection(frame):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(SNAPSHOT_DIR, f"motion_{ts}.jpg")
    cv2.imwrite(path, frame)
    threading.Thread(target=_on_motion_cb, args=(path,), daemon=True).start()


def _overlay(frame, motion):
    h, w  = frame.shape[:2]
    color = (0, 60, 220) if motion else (0, 185, 80)
    ov    = frame.copy()
    cv2.rectangle(ov, (0, 0), (w, 44), (8, 8, 12), -1)
    cv2.addWeighted(ov, 0.55, frame, 0.45, 0, frame)
    ts = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    cv2.putText(frame, ts, (12, 29),
                cv2.FONT_HERSHEY_SIMPLEX, 0.62, (190, 210, 255), 1, cv2.LINE_AA)
    label = "MOVIMIENTO" if motion else "EN VIVO"
    cv2.putText(frame, label, (w - 130, 29),
                cv2.FONT_HERSHEY_SIMPLEX, 0.56, color, 1, cv2.LINE_AA)
    x1, y1 = int(w * 0.12), int(h * 0.28)
    x2, y2 = int(w * 0.88), int(h * 0.72)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    return frame