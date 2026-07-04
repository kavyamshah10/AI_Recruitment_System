"""
session.py
-----------------------
Handles Streamlit session state.
"""

import streamlit as st


def initialize_session():
    """
    Initialize session variables.
    """

    defaults = {
        "logged_in": False,
        "user_type": None,
        "user_id": None,
        "username": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(user_id, username):
    """
    Login Candidate
    """

    st.session_state.logged_in = True
    st.session_state.user_type = "candidate"
    st.session_state.user_id = user_id
    st.session_state.username = username


def login_hr():
    """
    Login HR
    """

    st.session_state.logged_in = True
    st.session_state.user_type = "hr"
    st.session_state.user_id = None
    st.session_state.username = "HR"


def logout():
    """
    Logout current user
    """

    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.username = None