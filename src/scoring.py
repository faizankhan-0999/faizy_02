from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError


class AnalysisResult(BaseModel):
    overall_match_score: int = Field(..., ge=0, le=100)
    summary: str
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    gaps: list[str]
    actionable_improvements: list[str]
    recommended_keywords: list[str]
    interview_prep_topics: list[str]


def validate_and_format_analysis(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates raw dictionary response against Pydantic schema and clamps numerical scores.
    """
    try:
        # Clamp score explicitly before strict validation
        if "overall_match_score" in raw_data:
            score = int(raw_data["overall_match_score"])
            raw_data["overall_match_score"] = max(0, min(100, score))
            
        validated = AnalysisResult(**raw_data)
        return validated.model_dump()
    except (ValidationError, TypeError, ValueError) as err:
        raise ValueError(f"Model response structure validation failed: {str(err)}")
