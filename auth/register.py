"""
register.py
-----------------------------------------
Candidate Registration
"""

import streamlit as st

from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal
from database.models import User

from auth.password_hash import hash_password


def register_page():

    st.title("Candidate Registration")

    with st.form("register_form"):

        username = st.text_input("Username")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.form_submit_button("Register")

    # -----------------------------
    # Registration
    # -----------------------------

    if submit:

        username = username.strip()

        email = email.strip().lower()

        if not username:

            st.error("Username is required.")

            return

        if not email:

            st.error("Email is required.")

            return

        if not password:

            st.error("Password is required.")

            return

        if not confirm_password:

            st.error("Confirm Password is required.")

            return

        if password != confirm_password:

            st.error("Passwords do not match.")

            return

        db = SessionLocal()

        try:

            # -----------------------------
            # Username Exists
            # -----------------------------

            existing_username = (

                db.query(User)

                .filter(User.username == username)

                .first()

            )

            if existing_username:

                st.error("Username already exists.")

                return

            # -----------------------------
            # Email Exists
            # -----------------------------

            existing_email = (

                db.query(User)

                .filter(User.email == email)

                .first()

            )

            if existing_email:

                st.error("Email already exists.")

                return

            # -----------------------------
            # Create User
            # -----------------------------

            new_user = User(

                username=username,

                email=email,

                password_hash=hash_password(password)

            )

            db.add(new_user)

            db.commit()

            st.success("Registration Successful!")

            st.info("Please login with your registered email and password.")

            st.session_state.page = "login"

            st.rerun()

        except IntegrityError:

            db.rollback()

            st.error("Username or Email already exists.")

        except Exception as e:

            db.rollback()

            st.error(f"Registration Failed: {e}")

        finally:

            db.close()

    # -----------------------------
    # Back to Login
    # -----------------------------

    st.markdown("---")

    if st.button("Already have an account? Login"):

        st.session_state.page = "login"

        st.rerun()