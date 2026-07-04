"""
utils.py
------------------------------------
Utility functions for resume
upload and processing.
"""

import os
import uuid

from resume.parser import extract_resume_text
from resume.ocr import extract_text_from_scanned_pdf


# ==========================================
# Save Uploaded Resume
# ==========================================

def save_resume(uploaded_file, upload_folder):
    """
    Save uploaded resume with a
    unique filename.
    """

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    extension = os.path.splitext(uploaded_file.name)[1]

    unique_filename = (
        str(uuid.uuid4()) + extension
    )

    file_path = os.path.join(
        upload_folder,
        unique_filename
    )

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return uploaded_file.name, file_path


# ==========================================
# Delete Old Resume
# ==========================================

def delete_resume(file_path):
    """
    Delete previous resume if it exists.
    """

    if file_path and os.path.exists(file_path):
        os.remove(file_path)


# ==========================================
# Get Resume Text
# ==========================================

def get_resume_text(file_path):
    """
    Extract text from resume.
    If normal parsing fails,
    OCR is used automatically.
    """

    text = extract_resume_text(file_path)

    if len(text.strip()) < 20:
        text = extract_text_from_scanned_pdf(file_path)

    return text


# ==========================================
# Allowed File Check
# ==========================================

def allowed_resume(filename):
    """
    Check whether the uploaded
    file is supported.
    """

    extension = os.path.splitext(filename)[1].lower()

    return extension in [
        ".pdf",
        ".docx"
    ]


# ==========================================
# Resume Exists
# ==========================================

def resume_exists(file_path):
    """
    Check whether resume exists.
    """

    return os.path.exists(file_path)