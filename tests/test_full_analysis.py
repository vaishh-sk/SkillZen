import unittest
from io import BytesIO

import pymupdf

from app import app


class TestFullAnalysis(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def create_sample_pdf(self):

        document = pymupdf.open()
        page = document.new_page()

        page.insert_text(
            (72, 72),
            """
            Python Java SQL Flask Git
            Backend Developer
            """
        )

        pdf_bytes = document.tobytes()
        document.close()

        return pdf_bytes

    def test_complete_analysis(self):

        pdf_bytes = self.create_sample_pdf()

        response = self.client.post(
            "/analyze",
            data={
                "resume": (
                    BytesIO(pdf_bytes),
                    "sample_resume.pdf"
                ),
                "job_description": """
                    We need a Python developer with SQL,
                    Flask, Docker and AWS experience.
                """
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)

        result = response.get_json()

        self.assertEqual(result["status"], "success")

        self.assertIn(
            "Python",
            result["matching_skills"]["programming_languages"]
        )

        self.assertIn(
            "Docker",
            result["missing_skills"]["tools_and_platforms"]
        )

        self.assertIn(
            "AWS",
            result["missing_skills"]["tools_and_platforms"]
        )

        self.assertEqual(result["score"]["match_score"], 60.0)

        self.assertEqual(len(result["roadmap"]), 2)

    def test_missing_resume(self):

        response = self.client.post(
            "/analyze",
            data={
                "job_description": "Python developer with SQL and Flask experience."
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_job_description(self):

        pdf_bytes = self.create_sample_pdf()

        response = self.client.post(
            "/analyze",
            data={
                "resume": (
                    BytesIO(pdf_bytes),
                    "sample_resume.pdf"
                ),
                "job_description": ""
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()