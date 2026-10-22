import unittest
from unittest.mock import patch
from src.gemini_service import analyze_resume_match


class TestGeminiValidation(unittest.TestCase):

    def test_missing_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                analyze_resume_match("Resume sample", "Job sample", api_key="")


if __name__ == "__main__":
    unittest.main()
