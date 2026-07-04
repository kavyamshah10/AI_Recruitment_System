"""
login.py
-----------------------------------------
Login Page
"""

import streamlit as st

from sqlalchemy import or_

from database.database import SessionLocal
from database.models import User

from auth.password_hash import verify_password
from config import HR_NAME, HR_PASSWORD


def login():

    st.title("AI Recruitment System")

    st.markdown("---")

    login_type = st.radio(

        "Login As",

        [

            "Candidate",

            "HR"

        ]

    )

    # =====================================================
    # Candidate Login
    # =====================================================

    if login_type == "Candidate":

        st.subheader("Candidate Login")

        email = st.text_input("Email")

        password = st.text_input(

            "Password",

            type="password"

        )

        col1, col2 = st.columns(2)

        with col1:

            login_btn = st.button("Login")

        with col2:

            register_btn = st.button("Register")

        # ----------------------------
        # Register
        # ----------------------------

        if register_btn:

            st.session_state.page = "register"

            st.rerun()

        # ----------------------------
        # Login
        # ----------------------------

        if login_btn:

            email = email.strip().lower()

            db = SessionLocal()

            try:

                user = (

                    db.query(User)

                    .filter(
                        User.email == email
                    )

                    .first()

                )

                if user is None:

                    st.error("User not found.")

                    return

                if not verify_password(

                    password,

                    user.password_hash

                ):

                    st.error("Incorrect Password.")

                    return

                st.session_state.logged_in = True

                st.session_state.role = "candidate"

                st.session_state.user_id = user.id

                st.session_state.username = user.username

                st.success("Login Successful")

                st.rerun()

            finally:

                db.close()

    # =====================================================
    # HR Login
    # =====================================================

    else:

        st.subheader("HR Login")

        username = st.text_input("HR Name")

        password = st.text_input(

            "Password",

            type="password"

        )

        if st.button("Login"):

            if (

                username == HR_NAME

                and

                password == HR_PASSWORD

            ):

                st.session_state.logged_in = True

                st.session_state.role = "hr"

                st.session_state.username = username

                st.success("Login Successful")

                st.rerun()

            else:

                st.error(

                    "Invalid HR Credentials"

                )