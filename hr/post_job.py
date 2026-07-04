"""
post_job.py
-----------------------------------------
HR can post new jobs.
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Job


def post_job_page():

    st.subheader("Post New Job")

    # -----------------------------
    # Job Details Form
    # -----------------------------

    with st.form("post_job_form"):

        job_role = st.text_input(
            "Job Role"
        )

        required_skills = st.text_area(
            "Required Skills (Comma Separated)"
        )

        minimum_score = st.number_input(
            "Minimum Resume Score",
            min_value=0,
            max_value=100,
            value=70
        )

        # NEW FIELD
        experience = st.text_input(
            "Experience Required",
            placeholder="e.g. Fresher, 0-1 Years, 2+ Years"
        )

        # NEW FIELD
        salary = st.text_input(
            "Salary",
            placeholder="e.g. ₹4 LPA or ₹5-7 LPA"
        )

        # NEW FIELD
        location = st.text_input(
            "Location",
            placeholder="e.g. Mumbai, Pune, Remote"
        )

        job_description = st.text_area(
            "Job Description"
        )

        submit = st.form_submit_button(
            "Post Job"
        )

    # -----------------------------
    # Save Job
    # -----------------------------

    if submit:

        if (
            job_role.strip() == ""
            or required_skills.strip() == ""
            or job_description.strip() == ""
            or experience.strip() == ""
            or salary.strip() == ""
            or location.strip() == ""
        ):

            st.error("Please fill all fields.")

            return

        db = SessionLocal()

        try:

            job = Job(

                job_role=job_role,

                required_skills=required_skills,

                minimum_score=minimum_score,

                job_description=job_description,

                experience=experience,

                salary=salary,

                location=location,

                posted_by=st.session_state.username,

                total_applications=0,

                is_open=True

            )

            db.add(job)

            db.commit()

            st.success("Job Posted Successfully.")

            st.balloons()

        except Exception as e:

            db.rollback()

            st.error(f"Error : {e}")

        finally:

            db.close()