"""
app.py
-----------------------------------------
Main Entry Point
"""

import streamlit as st

from auth.login import login
from auth.register import register_page

from candidate.dashboard import dashboard as candidate_dashboard
from hr.dashboard import dashboard as hr_dashboard

from utils.helpers import load_css


# -----------------------------------------
# Streamlit Configuration
# -----------------------------------------

st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# Load CSS
# -----------------------------------------

load_css("assets/style.css")

# -----------------------------------------
# Initialize Session Variables
# -----------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "role" not in st.session_state:
    st.session_state.role = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None


# -----------------------------------------
# Routing
# -----------------------------------------

if not st.session_state.logged_in:

    if st.session_state.page == "login":

        login()

    elif st.session_state.page == "register":

        register_page()

else:

    if st.session_state.role == "candidate":

        candidate_dashboard()

    elif st.session_state.role == "hr":

        hr_dashboard()

    else:

        st.error("Invalid User Role")