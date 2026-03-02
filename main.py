# main.py

import time
from typing import Dict

from embedding import EmbeddingEngine
from similarity_engine import SimilarityEngine
from insight_generator import InsightGenerator
from utils import (
    load_case_database,
    validate_case_input,
    format_output,
    log
)
from config import CSV_DATA_PATH, EMBEDDING_DIM, TOP_K


# Main Pipeline

def main():

    try:
        start_time = time.time()

        # ---------------------------------------------------
        # Step 1: Load Case Database
        # ---------------------------------------------------

        log("Loading case database...")
        case_database: Dict = load_case_database(CSV_DATA_PATH)

        if not case_database:
            log("No cases found in database. Exiting.")
            return

        #  Initialize Embedding Engine
        
        log("Initializing embedding engine...")
        embedding_engine = EmbeddingEngine(embedding_dim=EMBEDDING_DIM)

        
        # Precompute Case Embeddings
        
        log("Generating embeddings for case database...")
        case_embeddings = {}

        for case_id, case_data in case_database.items():
            embedding = embedding_engine.generate_embedding(case_data)
            case_embeddings[case_id] = embedding

       
        # Initialize Similarity Engine
        

        log("Initializing similarity engine...")
        similarity_engine = SimilarityEngine(case_embeddings)

        
        # Initialize Insight Generator
        
        log("Initializing insight generator...")
        insight_generator = InsightGenerator(case_database)

        
        # Simulation Mode (Multiple Test Cases)
        

        test_cases = [
    {
        "case_id": "NEW_SKIN_001",
        "clinic_id": "CLINIC_001",
        "symptoms": ["itching", "red rash on neck"],
        "duration_days": 14,
        "doctor_notes": "Patient reports recent use of new cosmetic product.",
        "diagnosis": "",
        "treatment": "",
        "outcome": "",
        "recovery_days": None,
        "patient": {
            "age": 26,
            "gender": "Female"
        }
    },
    {
        "case_id": "NEW_SKIN_002",
        "clinic_id": "CLINIC_001",
        "symptoms": ["white patches on forearm", "mild dryness"],
        "duration_days": 120,
        "doctor_notes": "Non-itchy depigmented patches, gradually increasing in size.",
        "diagnosis": "",
        "treatment": "",
        "outcome": "",
        "recovery_days": None,
        "patient": {
            "age": 21,
            "gender": "Male"
        }
    },
    {
        "case_id": "NEW_SKIN_003",
        "clinic_id": "CLINIC_001",
        "symptoms": ["pus-filled pimples on cheeks", "oily skin"],
        "duration_days": 60,
        "doctor_notes": "Inflammatory acne lesions with occasional scarring.",
        "diagnosis": "",
        "treatment": "",
        "outcome": "",
        "recovery_days": None,
        "patient": {
            "age": 24,
            "gender": "Female"
        }
    }
]

        # Process Each Simulated Case
        for new_case in test_cases:

            log(f"\nProcessing Case: {new_case['case_id']}")

            # Validate Input
            validate_case_input(new_case)

            # Generate Query Embedding
            log("Generating query embedding...")
            query_embedding = embedding_engine.generate_embedding(new_case)

            # Retrieve Top-K Similar Cases
            log("Retrieving top similar cases...")
            top_matches = similarity_engine.retrieve_top_k(
                query_embedding,
                top_k=TOP_K
            )

            # Generate Insight (FIXED unpacking)
            log("Generating clinical insight...")
            insight_summary, confidence_reason = (
                insight_generator.generate_insight(top_matches)
            )

            # Format Output (Fixed structure)
            final_output = format_output(
                query_case_id=new_case["case_id"],
                top_matches=top_matches,
                insight={
                    "insight_summary": insight_summary,
                    "confidence_note": confidence_reason
                }
            )

            print(final_output)

       
        # Performance Measurement 
        

        end_time = time.time()
        total_time = end_time - start_time
        log(f"Total Execution Time: {total_time:.4f} seconds")

        log("Pipeline completed successfully.")

    except Exception as e:
        log(f"System Error: {str(e)}")



# MAIN


if __name__ == "__main__":
    main()