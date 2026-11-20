
import pymupdf


def extract_text_from_pdf(pdf_file):
    """
    Extract readable text from an uploaded PDF resume.

    Args:
        pdf_file: Uploaded PDF file object.

    Returns:
        Extracted resume text as a string.
    """

    pdf_bytes = pdf_file.read()

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        ) as pdf:

            extracted_text = ""

            for page in pdf:
                extracted_text += page.get_text() + "\n"

    except (pymupdf.FileDataError, ValueError) as error:
        raise ValueError(
            "Unable to read the PDF. Please upload a valid PDF file."
        ) from error

    if not extracted_text.strip():
        raise ValueError(
            "No readable text found in the PDF."
        )

    return extracted_text.strip()
