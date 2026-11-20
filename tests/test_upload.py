
import unittest
import requests


class TestUpload(unittest.TestCase):

    def test_upload(self):

        with open("tests/sample_resume.pdf", "rb") as resume:
            response = requests.post(
                "http://127.0.0.1:5000/analyze",
                files={
                    "resume": (
                        "sample_resume.pdf",
                        resume,
                        "application/pdf"
                    )
                },
                data={
                    "job_description": (
                        "Python SQL Flask Docker AWS "
                        "backend development experience"
                    )
                }
            )

        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertEqual(result["status"], "success")
        self.assertIn("score", result)


if __name__ == "__main__":
    unittest.main()

