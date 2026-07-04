"""
dashboard.py
-----------------------------------------
Candidate Dashboard
"""

import streamlit as st

from utils.helpers import load_css, page_title

from candidate.jobs import jobs_page
from candidate.upload_resume import upload_resume_page
from candidate.score import score_page
from candidate.status import status_page

from auth.session import logout


def dashboard():

    # Load CSS

    load_css("assets/style.css")

    # Page Title

    page_title("Candidate Dashboard")

    st.write(f"### Welcome, {st.session_state.username}")

    st.markdown("---")

    # Sidebar

    choice = st.sidebar.radio(

        "Navigation",

        [

            "🏠 Home",

            "📋 Available Jobs",

            "📄 Upload Resume",

            "📊 My Resume Score",

            "📌 Application Status",

            "🚪 Logout"

        ]

    )

    # -----------------------------
    # Home
    # -----------------------------

    if choice == "🏠 Home":

        st.subheader("Welcome to AI Recruitment System")

        st.info(
            """
            Complete the following steps:

            1. View Available Jobs

            2. Apply for a Job

            3. Upload Resume

            4. Check Resume Score

            5. View Application Status
            """
        )

    # -----------------------------
    # Jobs
    # -----------------------------

    elif choice == "📋 Available Jobs":

        jobs_page()

    # -----------------------------
    # Upload Resume
    # -----------------------------

    elif choice == "📄 Upload Resume":

        upload_resume_page()

    # -----------------------------
    # Resume Score
    # -----------------------------

    elif choice == "📊 My Resume Score":

        score_page()

    # -----------------------------
    # Status
    # -----------------------------

    elif choice == "📌 Application Status":

        status_page()

    # -----------------------------
    # Logout
    # -----------------------------

    elif choice == "🚪 Logout":

        logout()

        st.success("Logged out successfully.")

        st.rerun()