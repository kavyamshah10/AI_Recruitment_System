"""
status.py
-----------------------------------------
Display Candidate Application Status
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Application, Job


def status_page():

    st.subheader("Application Status")

    db = SessionLocal()

    try:

        applications = (

            db.query(Application)

            .filter(
                Application.user_id == st.session_state.user_id
            )

            .order_by(Application.id.desc())

            .all()

        )

        if not applications:

            st.warning(
                "You have not applied for any job."
            )

            return

        for application in applications:

            job = (

                db.query(Job)

                .filter(
                    Job.id == application.job_id
                )

                .first()

            )

            with st.container():

                st.markdown("---")

                st.write(
                    f"### {job.job_role}"
                )

                st.write(
                    f"Resume Score : {application.resume_score}/100"
                )

                if application.status == "Selected":

                    st.success(
                        f"Status : {application.status}"
                    )

                else:

                    st.error(
                        f"Status : {application.status}"
                    )

    finally:

        db.close()