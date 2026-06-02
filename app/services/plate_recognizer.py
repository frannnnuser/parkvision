import random
import string
import requests


class RecognitionResult:
    def __init__(self, plate: str, confidence: float, vehicle_type: str, simulated: bool = False):
        self.plate        = plate.upper().strip()
        self.confidence   = confidence
        self.vehicle_type = vehicle_type
        self.simulated    = simulated

    def to_dict(self):
        return {
            "plate":        self.plate,
            "confidence":   self.confidence,
            "vehicle_type": self.vehicle_type,
            "simulated":    self.simulated,
        }


def recognize(image_path: str) -> RecognitionResult:
    from flask import current_app
    api_key = current_app.config.get("PLATE_API_KEY", "")
    if api_key:
        result = _call_api(image_path, api_key)
        if result:
            return result
    return _simulate()


def _call_api(image_path: str, api_key: str):
    try:
        with open(image_path, "rb") as f:
            response = requests.post(
                "https://api.platerecognizer.com/v1/plate-reader/",
                data={"regions": ["pe", "cl", "ar", "br", "co", "mx"]},
                files={"upload": f},
                headers={"Authorization": f"Token {api_key}"},
                timeout=10,
            )
        if response.status_code != 201:
            return None
        results = response.json().get("results", [])
        if not results:
            return None
        best = results[0]
        return RecognitionResult(
            plate        = best["plate"],
            confidence   = round(best["score"], 4),
            vehicle_type = best.get("vehicle", {}).get("type", "car"),
            simulated    = False,
        )
    except Exception:
        return None


def _simulate() -> RecognitionResult:
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    numbers = "".join(random.choices(string.digits, k=3))
    return RecognitionResult(
        plate        = f"{letters}-{numbers}",
        confidence   = round(random.uniform(0.83, 0.99), 4),
        vehicle_type = random.choice(["car", "truck", "motorcycle"]),
        simulated    = True,
    )