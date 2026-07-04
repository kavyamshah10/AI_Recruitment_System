"""
apply_job.py
-----------------------------------------
Candidate applies for a job.
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Job, Application


def apply_job_page(job_id):
    """
    Apply for a selected job.
    """

    db = SessionLocal()

    # -----------------------------
    # Fetch Job
    # -----------------------------

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:

        st.error("Job not found.")

        db.close()

        return

    st.subheader("Apply Job")

    st.write(f"### {job.job_role}")

    st.write(f"**Required Skills:** {job.required_skills}")

    st.write(f"**Minimum Score:** {job.minimum_score}")

    st.markdown("---")

    # -----------------------------
    # Already Applied ?
    # -----------------------------

    application = (

        db.query(Application)

        .filter(

            Application.user_id == st.session_state.user_id,

            Application.job_id == job.id

        )

        .first()

    )

    if application:

        st.warning(
            "You have already applied for this job."
        )

        db.close()

        return

    # -----------------------------
    # Instructions
    # -----------------------------

    st.info(
        """
        Before applying:

        • Upload your latest resume.

        • Resume score will be calculated.

        • Status will be generated automatically.
        """
    )

    if st.button("Confirm Apply"):

        st.session_state.apply_job = job.id

        st.success(
            "Application request saved."
        )

        st.info(
            "Now go to 'Upload Resume' to complete your application."
        )

    db.close()