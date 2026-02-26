# database.py

from pymongo import MongoClient
from typing import Dict, Any

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)
db = client["ccms_training"]
collection = db["clinic_cases"]


def fetch_case_database() -> Dict[str, Dict[str, Any]]:
    """
    Fetch patient records from MongoDB
    and convert to required internal format.
    """

    case_database = {}

    try:
        records = collection.find({})

        for record in records:

            case_id = str(record.get("case_id"))

            case_database[case_id] = {
                # Your actual fields
                "symptoms": record.get("symptoms", []),
                "diagnosis": "",  # Not present in DB
                "treatment": "",  # Not present in DB
                "notes": record.get("doctor_notes", ""),
                "duration_days": record.get("duration_days"),
                "clinic_id": record.get("clinic_id"),
                "patient_age": None,
                "patient_gender": None,
                "outcome": "",
                "recovery_days": None,
            }

    except Exception as e:
        print("MongoDB Connection Error:", e)

    return case_database