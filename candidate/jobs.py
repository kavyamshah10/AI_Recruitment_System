"""
jobs.py
-----------------------------------------
Display all active jobs and allow
candidate to apply.
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Job

from candidate.apply_job import apply_job_page


def jobs_page():

    st.subheader("Available Jobs")

    db = SessionLocal()

    jobs = (
        db.query(Job)
        .filter(Job.is_open == True)
        .order_by(Job.id.desc())
        .all()
    )

    if not jobs:

        st.info("No job openings available.")

        db.close()

        return

    for job in jobs:

        with st.container():

            st.markdown("---")

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"### {job.job_role}"
                )

                st.write(
                    f"**Required Skills:** {job.required_skills}"
                )

                st.write(
                    f"**Minimum Score:** {job.minimum_score}"
                )

                st.write(
                    f"**Applications Received:** {job.total_applications}"
                )

            with col2:

                if st.button(
                    "Apply",
                    key=f"apply_{job.id}"
                ):

                    st.session_state.selected_job = job.id

                    st.rerun()

    db.close()

    # ----------------------------------
    # Open Apply Page
    # ----------------------------------

    if "selected_job" in st.session_state:

        st.markdown("---")

        apply_job_page(
            st.session_state.selected_job
        )