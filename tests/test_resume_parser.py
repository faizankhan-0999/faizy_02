import io
import unittest
from src.resume_parser import extract_text_from_pdf


class TestResumeParser(unittest.TestCase):

    def test_empty_input(self):
        text, err = extract_text_from_pdf(None)
        self.assertEqual(text, "")
        self.assertIn("No file provided", err)

    def test_oversized_file(self):
        # Create dummy buffer exceeding 5MB
        large_buffer = io.BytesIO(b"0" * (6 * 1024 * 1024))
        text, err = extract_text_from_pdf(large_buffer, max_size_mb=5.0)
        self.assertEqual(text, "")
        self.assertIn("exceeds", err)


if __name__ == "__main__":
    unittest.main()
