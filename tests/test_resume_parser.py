
import unittest
from io import BytesIO

import pymupdf

from backend.resume_parser import extract_text_from_pdf


class TestResumeParser(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        # Create a sample PDF in memory
        document = pymupdf.open()

        page = document.new_page()

        page.insert_text(
            (72, 72),
            "Python SQL Flask Backend Developer"
        )

        pdf_bytes = document.tobytes()
        document.close()

        # Pass the PDF to our extraction function
        pdf_file = BytesIO(pdf_bytes)

        extracted_text = extract_text_from_pdf(pdf_file)

        # Verify extracted content
        self.assertIn("Python", extracted_text)
        self.assertIn("SQL", extracted_text)
        self.assertIn("Flask", extracted_text)

    def test_empty_pdf(self):
        empty_file = BytesIO(b"")

        with self.assertRaises(ValueError):
            extract_text_from_pdf(empty_file)


if __name__ == "__main__":
    unittest.main()
