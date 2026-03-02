# utils.py

import pandas as pd
from typing import Dict, Any



# DATA LOADER

def load_case_database(file_path: str) -> Dict[str, Dict[str, Any]]:
    

    df = pd.read_csv(file_path)
    case_database = {}

    for _, row in df.iterrows():

        case_id = str(row["case_id"])

        # Convert symptoms string to list
        symptoms_raw = str(row["symptoms"])
        symptoms_list = [s.strip() for s in symptoms_raw.split(",")]

        case_database[case_id] = {
            "symptoms": symptoms_list,
            "diagnosis": row.get("diagnosis", ""),
            "treatment": row.get("treatment", ""),
            "notes": row.get("doctor_notes", ""),
            "duration_days": row.get("duration_days", None),
            "clinic_id": row.get("clinic_id", None),
            "patient_age": row.get("patient.age", None),
            "patient_gender": row.get("patient.gender", None),
            "outcome": row.get("outcome", ""),
            "recovery_days": row.get("recovery_days", None),
        }

    return case_database


# INPUT VALIDATION


def validate_case_input(case_input: Dict[str, Any]) -> bool:
   

    required_fields = ["symptoms"]

    for field in required_fields:
        if field not in case_input:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(case_input["symptoms"], list):
        raise ValueError("Symptoms must be provided as a list.")

    return True



# OUTPUT FORMATTER

def format_output(
    query_case_id: str,
    top_matches,
    insight: Dict[str, Any]
) -> str:
    """
    Format final structured output.
    """

    result = "\n==== CCMS-AI RESULT ====\n\n"

    result += f"Query Case ID: {query_case_id}\n\n"

    result += "🔎 Top Similar Cases:\n"
    for case_id, similarity in top_matches:
        result += f"- Case ID: {case_id} | Similarity: {similarity:.4f}\n"

    result += "\n🩺 Predicted Diagnosis:\n"
    result += insight.get("most_common_diagnosis", "N/A") + "\n"

    result += "\n💊 Suggested Treatment:\n"
    result += insight.get("recommended_treatment", "N/A") + "\n"

    result += "\n📊 Confidence:\n"
    result += insight.get("confidence_note", "N/A") + "\n"

    result += "\n===============================================\n"

    return result


# LOGGER


def log(message: str) -> None:
    """
    Simple console logger.
    """
    print(f"[CCMS-AI] {message}")