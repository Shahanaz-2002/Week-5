# database.py

from pymongo import MongoClient
from typing import Dict, Any
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def fetch_case_database() -> Dict[str, Dict[str, Any]]:
    case_database = {}

    try:
        records = collection.find({})

        for record in records:
            case_id = str(record.get("case_id"))

            case_database[case_id] = {
                "symptoms": record.get("symptoms", []),
                "diagnosis": record.get("diagnosis", ""),
                "treatment": record.get("treatment", ""),
                "notes": record.get("doctor_notes", ""),

                # NEW
                "embedding": record.get("embedding", None),
                "embedding_version": record.get("embedding_version", None)
            }

    except Exception as e:
        print("MongoDB Error:", e)

    return case_database