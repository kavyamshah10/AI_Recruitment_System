"""
validators.py
-----------------------------------
Common validation functions used
throughout the project.
"""

import os
import re

from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE



def is_empty(*fields):
    """
    Returns True if any field is empty.
    """

    for field in fields:
        if str(field).strip() == "":
            return True

    return False


# ============================================
# Email Validation
# ============================================

def validate_email(email):
    """
    Validate email format.
    """

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return re.match(pattern, email) is not None



def validate_username(username):
    """
    Username must be at least
    4 characters long.
    """

    return len(username) >= 4



def validate_password(password):
    """
    Password must be at least
    6 characters long.
    """

    return len(password) >= 6


# ============================================
# Resume File Validation
# ============================================

def validate_resume(file):
    """
    Validate uploaded resume.
    """

    if file is None:
        return False, "Please upload a resume."

    filename = file.name

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        return (
            False,
            "Only PDF and DOCX files are allowed."
        )

    if file.size > MAX_FILE_SIZE:

        return (
            False,
            "Maximum file size is 5 MB."
        )

    return True, "Valid File"


# ============================================
# Score Validation
# ============================================

def validate_score(score):
    """
    Score should be between
    0 and 100.
    """

    return 0 <= score <= 100


# ============================================
# Minimum Score Validation
# ============================================

def validate_minimum_score(score):
    """
    HR should enter
    minimum score between
    0 and 100.
    """

    return 0 <= score <= 100