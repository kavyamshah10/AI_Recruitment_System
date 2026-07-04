"""
ocr.py
------------------------------------
Extract text from scanned PDF
or image resumes using OCR.
"""

import fitz
import pytesseract

from PIL import Image


def extract_text_from_scanned_pdf(pdf_path):
    """
    Extract text from scanned PDF
    using OCR.
    """

    text = ""

    try:

        document = fitz.open(pdf_path)

        for page in document:

            pix = page.get_pixmap(dpi=300)

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            page_text = pytesseract.image_to_string(image)

            text += page_text + "\n"

        document.close()

    except Exception as e:

        print("OCR Error:", e)

    return text


# ==========================================
# OCR From Image
# ==========================================

def extract_text_from_image(image_path):
    """
    Extract text from image resume.
    """

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:

        print("Image OCR Error:", e)

        return ""