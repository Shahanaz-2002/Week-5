# database.py

from pymongo import MongoClient
from typing import Dict, Any
import numpy as np
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


# ---------------------------------------------------
# Fetch full case database
# ---------------------------------------------------
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

                # Stored embeddings (Day 4)
                "embedding": record.get("embedding", None),
                "embedding_version": record.get("embedding_version", None)
            }

    except Exception as e:
        print("MongoDB Error:", e)

    return case_database


# ---------------------------------------------------
# Fetch only embeddings for similarity search
# ---------------------------------------------------
def fetch_case_embeddings() -> Dict[str, np.ndarray]:
    """
    Returns:
        {
            case_id: numpy_embedding_vector
        }
    """
    case_embeddings = {}

    try:
        records = collection.find({"embedding": {"$exists": True}})

        for record in records:
            case_id = str(record.get("case_id"))
            embedding = record.get("embedding")

            if embedding is not None:
                case_embeddings[case_id] = np.array(embedding)

    except Exception as e:
        print("MongoDB Error:", e)

    return case_embeddings