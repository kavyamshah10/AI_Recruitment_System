"""
dashboard.py
-----------------------------------------
HR Dashboard
"""

import streamlit as st

from utils.helpers import load_css, page_title

from hr.post_job import post_job_page
from hr.manage_jobs import manage_jobs_page
from hr.candidate_table import candidate_details_page
from hr.top_candidates import top_candidates_page
from hr.chatbot import chatbot_page

from auth.session import logout


def dashboard():

    load_css("assets/style.css")

    page_title("HR Dashboard")

    st.write(f"### Welcome, {st.session_state.username}")

    st.markdown("---")

    menu = st.sidebar.radio(

        "Navigation",

        [

            "🏠 Dashboard",

            "➕ Post Job",

            "📋 Manage Jobs",

            "👥 Candidate Details",

            "🏆 Top 3 Candidates",

            "📊 Candidate Status",

            "🤖 AI Chatbot",

            "🚪 Logout"

        ]

    )

    # ----------------------------------
    # Dashboard
    # ----------------------------------

    if menu == "🏠 Dashboard":

        st.subheader("AI Recruitment System")

        st.info(
            """
            HR Features

            • Post New Job

            • View Posted Jobs

            • View Candidate Details

            • View Top 3 Candidates

            • View Selected & Rejected Candidates

            • Search Candidates using AI Chatbot
            """
        )

    # ----------------------------------
    # Post Job
    # ----------------------------------

    elif menu == "➕ Post Job":

        post_job_page()

    # ----------------------------------
    # Manage Jobs
    # ----------------------------------

    elif menu == "📋 Manage Jobs":

        manage_jobs_page()

    # ----------------------------------
    # Candidate Details
    # ----------------------------------

    elif menu == "👥 Candidate Details":

        candidate_details_page()

    # ----------------------------------
    # Top Candidates
    # ----------------------------------

    elif menu == "🏆 Top 3 Candidates":

        top_candidates_page()

    # ----------------------------------
    # Candidate Status
    # ----------------------------------

    elif menu == "📊 Candidate Status":

        option = st.radio(

            "Select",

            [

                "Selected Candidates",

                "Rejected Candidates"

            ]

        )

        candidate_details_page(option)

    # ----------------------------------
    # AI Chatbot
    # ----------------------------------

    elif menu == "🤖 AI Chatbot":

        chatbot_page()

    # ----------------------------------
    # Logout
    # ----------------------------------

    elif menu == "🚪 Logout":

        logout()

        st.success("Logged out successfully.")

        st.rerun()