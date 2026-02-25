from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from embedding import EmbeddingEngine
from similarity_engine import SimilarityEngine
from insight_generator import InsightGenerator
from utils import load_case_database, validate_case_input

app = FastAPI()

# Load database once
case_database = load_case_database(
    r"D:\chiselon\Week 0\Week_0_Prep_Week_Ssample Data_clinic_cases.csv"
)

embedding_engine = EmbeddingEngine(embedding_dim=128)

case_embeddings = {}
for case_id, case_data in case_database.items():
    case_embeddings[case_id] = embedding_engine.generate_embedding(case_data)

similarity_engine = SimilarityEngine(case_embeddings)
insight_generator = InsightGenerator(case_database)


class CaseRequest(BaseModel):
    symptoms: List[str]
    doctor_notes: str


@app.post("/analyze-case")
def analyze_case(request: CaseRequest):

    new_case = {
        "symptoms": request.symptoms,
        "notes": request.doctor_notes,
        "diagnosis": ""
    }

    validate_case_input(new_case)

    query_embedding = embedding_engine.generate_embedding(new_case)

    top_matches = similarity_engine.retrieve_top_k(
        query_embedding,
        top_k=3
    )

    insight = insight_generator.generate_insight(top_matches)

    return {
        "top_similar_cases": [
            {
                "case_id": case_id,
                "similarity_score": score
            }
            for case_id, score in top_matches
        ],
        "predicted_diagnosis": insight["most_common_diagnosis"],
        "suggested_treatment": insight["recommended_treatment"],
        "confidence": insight["confidence_note"]
    }