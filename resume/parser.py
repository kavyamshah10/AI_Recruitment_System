"""
parser.py
------------------------------------
Reads PDF and DOCX resumes
and returns extracted text.
"""

import fitz  # PyMuPDF
from docx import Document
import os


def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF resume.
    """

    text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:
        print(f"PDF Error: {e}")

    return text


def extract_docx_text(docx_path):
    """
    Extract text from a DOCX resume.
    """

    text = ""

    try:
        document = Document(docx_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    except Exception as e:
        print(f"DOCX Error: {e}")

    return text


def extract_resume_text(file_path):
    """
    Automatically detect the file type
    and extract text.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    else:
        raise ValueError(
            "Only PDF and DOCX resumes are supported."
        )