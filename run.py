"""
run.py — Entry point for ParkVision.
Production: gunicorn run:app --workers 1 --threads 4 --bind 0.0.0.0:5000
Development: python run.py
"""

import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app({
    "SECRET_KEY":            os.getenv("SECRET_KEY", "dev-secret"),
    "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///parkvision.db"),
    "PLATE_API_KEY":         os.getenv("PLATE_RECOGNIZER_API_KEY", ""),
    "CAMERA_COOLDOWN":       int(os.getenv("CAMERA_COOLDOWN", 8)),
})

if __name__ == "__main__":
    app.run(
        host     = "0.0.0.0",
        port     = int(os.getenv("PORT", 5000)),
        debug    = os.getenv("FLASK_DEBUG", "false").lower() == "true",
        threaded = True,
    )
