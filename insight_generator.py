# insight_generator.py

from typing import Dict, List, Tuple
from collections import Counter


class InsightGenerator:

    def __init__(self, case_database: Dict[str, Dict]):
        self.case_database = case_database

    
    # Public Method
    

    def generate_insight(
        self,
        top_matches: List[Tuple[str, float]]
    ) -> Tuple[str, str]:

        
        # Case 1: No Similar Cases Found
        
        if not top_matches:
            return (
                "No similar historical cases found.",
                "Insufficient similarity data."
            )

        diagnoses = []
        treatments = []

        
        # Collect Diagnosis & Treatment
        
        for case_id, score in top_matches:
            case_data = self.case_database.get(case_id, {})

            diagnosis = case_data.get("diagnosis")
            treatment = case_data.get("treatment")

            if diagnosis:
                diagnoses.append(diagnosis)

            if treatment:
                treatments.append(treatment)

        most_common_diagnosis = self._most_common(diagnoses)
        recommended_treatment = self._most_common(treatments)

        
        # Smart Summary Generation        
        summary = self._generate_summary(
            most_common_diagnosis,
            recommended_treatment
        )

        
        # Confidence Calculation
        
        confidence = self._generate_confidence(top_matches)

        return summary, confidence

    
    # Generate Summary
    

    @staticmethod
    def _generate_summary(
        diagnosis: str,
        treatment: str
    ) -> str:

        if diagnosis == "insufficient data" and treatment == "insufficient data":
            return (
                "Similar cases were identified, but structured diagnosis "
                "and treatment data are not available for recommendation."
            )

        if diagnosis != "insufficient data" and treatment == "insufficient data":
            return (
                f"In similar past cases, patients were commonly diagnosed with "
                f"{diagnosis}. Treatment patterns were not consistently recorded."
            )

        if diagnosis == "insufficient data" and treatment != "insufficient data":
            return (
                f"In similar past cases, patients responded well to "
                f"{treatment}, although diagnosis data was limited."
            )

        return (
            f"In similar past cases, patients were commonly diagnosed with "
            f"{diagnosis} and responded well to {treatment}."
        )

    
    # Most Common Item
   
    @staticmethod
    def _most_common(items: List[str]) -> str:
        if not items:
            return "insufficient data"
        return Counter(items).most_common(1)[0][0]

    
    # Confidence Score (Improved)
    

    @staticmethod
    def _generate_confidence(
        top_matches: List[Tuple[str, float]]
    ) -> str:

        if not top_matches:
            return "Insufficient similarity data."

        scores = [score for _, score in top_matches]

        avg_score = sum(scores) / len(scores)
        max_score = max(scores)

        # Confidence decision using both avg and strongest match
        if avg_score > 0.85 and max_score > 0.9:
            return "High confidence based on strong similarity with historical cases."
        elif avg_score > 0.65:
            return "Moderate confidence based on similarity patterns."
        else:
            return "Low similarity confidence. Clinical review advised."