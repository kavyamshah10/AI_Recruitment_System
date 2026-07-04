"""
score.py
-----------------------------------------
Display Candidate Resume Score
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Candidate


def score_page():

    st.subheader("My Resume Score")

    db = SessionLocal()

    try:

        candidate = (
            db.query(Candidate)
            .filter(
                Candidate.user_id == st.session_state.user_id
            )
            .first()
        )

        if candidate is None:

            st.warning(
                "No resume uploaded yet."
            )

            return

        st.metric(

            label="Resume Score",

            value=f"{candidate.resume_score}/100"

        )

        if candidate.resume_score >= 80:

            st.success("Excellent Resume")

        elif candidate.resume_score >= 60:

            st.info("Good Resume")

        else:

            st.error(
                "Improve your resume to increase your score."
            )

    finally:

        db.close()