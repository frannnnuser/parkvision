import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from ..services.plate_recognizer import recognize
from ..services.parking          import process_plate
from ._helpers                   import success, error

bp      = Blueprint("records", __name__)
ALLOWED = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


@bp.get("/")
def list_records():
    from ..models.record import ParkingRecord
    limit = min(int(request.args.get("limit", 100)), 500)
    rows  = ParkingRecord.query.order_by(
        ParkingRecord.entry_time.desc()
    ).limit(limit).all()
    return success([r.to_dict() for r in rows])


@bp.post("/upload")
def upload_image():
    if "image" not in request.files:
        return error("No image provided")
    file = request.files["image"]
    ext  = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED:
        return error("Invalid file type")

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    filename   = f"upload_{secure_filename(file.filename)}"
    filepath   = os.path.join(upload_dir, filename)
    file.save(filepath)

    result = recognize(filepath)
    event  = process_plate(
        plate      = result.plate,
        confidence = result.confidence,
        image_path = filepath,
        source     = "upload",
        simulated  = result.simulated,
    )
    return success(event.to_dict())


@bp.post("/manual")
def manual_entry():
    data  = request.get_json(silent=True) or {}
    plate = data.get("plate", "").upper().strip()
    if not plate:
        return error("plate is required")
    event = process_plate(plate=plate, source="manual")
    return success(event.to_dict())