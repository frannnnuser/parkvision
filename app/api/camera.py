import json
import queue
import time
from flask import Blueprint, request, Response, current_app, stream_with_context
from ..services           import camera as cam_svc
from ..services.plate_recognizer import recognize
from ..services.parking   import process_plate
from ._helpers            import success, error

bp           = Blueprint("camera", __name__)
_event_queue = queue.Queue(maxsize=100)


def _on_motion(snap_path: str):
    from run import app
    result = recognize(snap_path)
    with app.app_context():
        try:
            event = process_plate(
                plate      = result.plate,
                confidence = result.confidence,
                image_path = snap_path,
                source     = "camera",
                simulated  = result.simulated,
            )
            _push(event.to_dict())
        except Exception as e:
            current_app.logger.error("Camera detection error: %s", e)


def _push(data):
    try:
        _event_queue.put_nowait(data)
    except queue.Full:
        _event_queue.get_nowait()
        _event_queue.put_nowait(data)


@bp.post("/start")
def start():
    d        = request.get_json(silent=True) or {}
    cooldown = int(current_app.config.get("CAMERA_COOLDOWN", 8))
    ok, msg  = cam_svc.start(
        mode      = d.get("mode", "webcam"),
        index     = int(d.get("index", 0)),
        url       = d.get("url", ""),
        cooldown  = cooldown,
        on_motion = _on_motion,
    )
    return success({"message": msg}) if ok else error(msg, 409)


@bp.post("/stop")
def stop():
    ok, msg = cam_svc.stop()
    return success({"message": msg})


@bp.get("/status")
def status():
    return success(cam_svc.get_status())


@bp.post("/capture")
def capture():
    path = cam_svc.capture_frame()
    if not path:
        b64 = (request.get_json(silent=True) or {}).get("frame_b64", "")
        if b64:
            path = cam_svc.save_b64_frame(b64)
    if not path:
        return error("No active camera frame", 422)

    result = recognize(path)
    event  = process_plate(
        plate      = result.plate,
        confidence = result.confidence,
        image_path = path,
        source     = "camera",
        simulated  = result.simulated,
    )
    _push(event.to_dict())
    return success(event.to_dict())


@bp.get("/stream")
def stream():
    def generate():
        while cam_svc.get_status()["running"]:
            jpg = cam_svc.get_frame()
            if jpg:
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
            time.sleep(0.033)
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


@bp.get("/events")
def events():
    def generate():
        yield "retry: 2000\n\n"
        while True:
            try:
                ev = _event_queue.get(timeout=20)
                yield f"data: {json.dumps(ev)}\n\n"
            except queue.Empty:
                yield ": ping\n\n"
    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )