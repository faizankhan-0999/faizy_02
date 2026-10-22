import json
import os
from typing import Dict, Any
from google import genai
from google.genai import types
from src.scoring import validate_and_format_analysis


ANALYSIS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "overall_match_score": {"type": "INTEGER", "description": "Match score from 0 to 100"},
        "summary": {"type": "STRING", "description": "Brief executive summary of qualification fit"},
        "matched_skills": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Skills present in both resume and job description"
        },
        "missing_skills": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Critical job requirements completely missing from resume"
        },
        "strengths": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Key candidate qualifications alignment highlights"
        },
        "gaps": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Underrepresented or unmentioned experience areas"
        },
        "actionable_improvements": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Specific resume bullet point or phrasing suggestions"
        },
        "recommended_keywords": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "High-impact job description keywords to incorporate"
        },
        "interview_prep_topics": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Technical or behavioral topics to review for interviews"
        }
    },
    "required": [
        "overall_match_score",
        "summary",
        "matched_skills",
        "missing_skills",
        "strengths",
        "gaps",
        "actionable_improvements",
        "recommended_keywords",
        "interview_prep_topics"
    ]
}


def analyze_resume_match(
    resume_text: str,
    job_description: str,
    job_title: str = "",
    company: str = "",
    api_key: str = None
) -> Dict[str, Any]:
    """
    Sends resume and job description to Gemini 2.5 Flash using official google-genai SDK.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("Missing Gemini API Key. Please provide it in Streamlit Secrets or environment variables.")

    client = genai.Client(api_key=key)

    # Restrict input prompts to reasonable character lengths
    clean_resume = resume_text[:12000]
    clean_job = job_description[:8000]

    system_instruction = (
        "You are an expert HR AI ATS auditor and talent acquisition specialist. "
        "Analyze the provided resume against the job description strictly objectively. "
        "Do NOT invent candidate qualifications or experience not explicitly written in the resume. "
        "Distinguish between skills missing vs skills merely unmentioned. "
        "Never consider or evaluate personal, sensitive, demographic, or non-professional traits. "
        "Evaluate solely based on hard skills, soft skills, relevant experience, tools, and technical fit."
    )

    user_prompt = f"""
TARGET ROLE: {job_title if job_title else 'Specified Job Role'}
COMPANY: {company if company else 'Target Employer'}

RESUME TEXT:
{clean_resume}

JOB DESCRIPTION:
{clean_job}
"""

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2,
        response_mime_type="application/json",
        response_schema=ANALYSIS_SCHEMA,
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=config,
        )

        if not response.text:
            raise RuntimeError("Empty response received from Gemini API.")

        parsed_json = json.loads(response.text)
        return validate_and_format_analysis(parsed_json)

    except Exception as exc:
        raise RuntimeError(f"Gemini API Analysis failed: {str(exc)}")
