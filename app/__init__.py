from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # ── Default config ────────────────────────────────────────────────────────
    app.config.setdefault("SECRET_KEY", "change-me-in-production")
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///parkvision.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("UPLOAD_FOLDER", "static/uploads")
    app.config.setdefault("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
    app.config.setdefault("PLATE_API_KEY", "")
    app.config.setdefault("CAMERA_COOLDOWN", 8)
    app.config.setdefault("MOTION_THRESHOLD", 3000)

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    import os
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ── Register blueprints ───────────────────────────────────────────────────
    from .api.vehicles import bp as vehicles_bp
    from .api.records import bp as records_bp
    from .api.camera import bp as camera_bp
    from .api.dashboard import bp as dashboard_bp
    from .api.slots import bp as slots_bp

    app.register_blueprint(vehicles_bp,  url_prefix="/api/vehicles")
    app.register_blueprint(records_bp,   url_prefix="/api/records")
    app.register_blueprint(camera_bp,    url_prefix="/api/camera")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(slots_bp,     url_prefix="/api/slots")

    # ── Main UI route ─────────────────────────────────────────────────────────
    from flask import render_template

    @app.route("/")
    def index():
        return render_template("index.html")

    # ── DB seed on first run ──────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed(app)

    return app


def _seed(app):
    from .models.slot import ParkingSlot
    from .models.vehicle import Vehicle

    if ParkingSlot.query.count() == 0:
        slots = [
            ParkingSlot(code=f"{'AB'[lvl]}{i:02d}", level=lvl + 1)
            for lvl in range(2)
            for i in range(1, 16)
        ]
        db.session.add_all(slots)

    if Vehicle.query.count() == 0:
        samples = [
            ("ABC-123", "Carlos Mendoza",  "Toyota",     "Corolla",  "Blanco", 2020),
            ("DEF-456", "María García",    "Hyundai",    "Tucson",   "Negro",  2021),
            ("GHI-789", "Pedro Rojas",     "Kia",        "Sportage", "Rojo",   2019),
            ("JKL-012", "Ana Torres",      "Volkswagen", "Golf",     "Plata",  2022),
            ("MNO-345", "Luis Castillo",   "Nissan",     "Sentra",   "Azul",   2018),
        ]
        vehicles = [
            Vehicle(plate=p, owner_name=n, brand=b, model=m, color=c, year=y)
            for p, n, b, m, c, y in samples
        ]
        db.session.add_all(vehicles)

    db.session.commit()
