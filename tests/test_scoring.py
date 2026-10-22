import unittest
from src.scoring import validate_and_format_analysis


class TestScoring(unittest.TestCase):

    def test_valid_payload(self):
        payload = {
            "overall_match_score": 85,
            "summary": "Great match",
            "matched_skills": ["Python", "Streamlit"],
            "missing_skills": ["Docker"],
            "strengths": ["Strong engineering background"],
            "gaps": ["Lacks containerization"],
            "actionable_improvements": ["Add Docker projects"],
            "recommended_keywords": ["CI/CD"],
            "interview_prep_topics": ["System design"]
        }
        res = validate_and_format_analysis(payload)
        self.assertEqual(res["overall_match_score"], 85)

    def test_score_clamping(self):
        payload = {
            "overall_match_score": 120,  # Invalid out of range
            "summary": "Over high",
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "gaps": [],
            "actionable_improvements": [],
            "recommended_keywords": [],
            "interview_prep_topics": []
        }
        res = validate_and_format_analysis(payload)
        self.assertEqual(res["overall_match_score"], 100)


if __name__ == "__main__":
    unittest.main()
