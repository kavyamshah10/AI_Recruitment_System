"""
config.py
-----------
Central configuration file for the AI Recruitment System.
Stores database settings, HR credentials, file upload settings,
and application constants.
"""

from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

HR_NAME = os.getenv("HR_NAME")

HR_PASSWORD = os.getenv("HR_PASSWORD")


UPLOAD_FOLDER = "uploads/resumes"

ALLOWED_EXTENSIONS = [
    ".pdf",
    ".docx"
]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


MAX_SCORE = 100


STATUS_SELECTED = "Selected"
STATUS_REJECTED = "Rejected"


JOB_OPEN = "Open"
JOB_CLOSED = "Closed"


PRIMARY_COLOR = "#2563EB"
SECONDARY_COLOR = "#7C3AED"
SUCCESS_COLOR = "#16A34A"
DANGER_COLOR = "#DC2626"
BACKGROUND_COLOR = "#F8FAFC"