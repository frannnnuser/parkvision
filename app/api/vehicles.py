from flask import Blueprint, request
from .. import db
from ..models.vehicle import Vehicle
from ._helpers        import success, error, validate_json

bp = Blueprint("vehicles", __name__)


@bp.get("/")
def list_vehicles():
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return success([v.to_dict() for v in vehicles])


@bp.post("/")
@validate_json("plate")
def create_vehicle():
    data  = request.get_json()
    plate = data["plate"].upper().strip()

    if Vehicle.query.filter_by(plate=plate).first():
        return error("Plate already registered", 409)

    vehicle = Vehicle(
        plate        = plate,
        owner_name   = data.get("owner_name"),
        owner_doc    = data.get("owner_doc"),
        brand        = data.get("brand"),
        model        = data.get("model"),
        color        = data.get("color"),
        year         = data.get("year"),
        vehicle_type = data.get("vehicle_type", "car"),
        authorized   = data.get("authorized", True),
        notes        = data.get("notes"),
    )
    db.session.add(vehicle)
    db.session.commit()
    return success(vehicle.to_dict(), 201)


@bp.get("/<int:vid>")
def get_vehicle(vid):
    vehicle = Vehicle.query.get_or_404(vid)
    return success(vehicle.to_dict())


@bp.patch("/<int:vid>")
def update_vehicle(vid):
    vehicle = Vehicle.query.get_or_404(vid)
    data    = request.get_json(silent=True) or {}
    fields  = ["owner_name", "owner_doc", "brand", "model",
               "color", "year", "vehicle_type", "authorized", "notes"]
    for field in fields:
        if field in data:
            setattr(vehicle, field, data[field])
    db.session.commit()
    return success(vehicle.to_dict())


@bp.delete("/<int:vid>")
def delete_vehicle(vid):
    vehicle = Vehicle.query.get_or_404(vid)
    db.session.delete(vehicle)
    db.session.commit()
    return success({"deleted": vid})
