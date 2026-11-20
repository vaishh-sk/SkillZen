import unittest

from backend.jd_parser import extract_job_description_text


class TestJDParser(unittest.TestCase):

    def test_clean_job_description(self):
        jd = """
        We are looking for a Python Developer.
        Candidate should know Python, SQL and Flask.
        """

        result = extract_job_description_text(jd)

        self.assertIn("Python Developer.", result)
        self.assertNotIn("\n", result)

    def test_empty_job_description(self):
        with self.assertRaises(ValueError):
            extract_job_description_text("")

    def test_short_job_description(self):
        with self.assertRaises(ValueError):
            extract_job_description_text("Python developer")

    def test_whitespace_job_description(self):
        with self.assertRaises(ValueError):
            extract_job_description_text("   \n   ")


if __name__ == "__main__":
    unittest.main()