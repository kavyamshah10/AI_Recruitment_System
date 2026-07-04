"""
candidate_table.py
-----------------------------------------
View Candidate Details
"""

import streamlit as st

from database.database import SessionLocal
from database.models import (
    Application,
    Job,
    Candidate
)

def candidate_details_page(filter_status=None):

    st.subheader("Candidate Details")

    db = SessionLocal()

    try:

        query = db.query(Application)

        if filter_status == "Selected Candidates":

            query = query.filter(
                Application.status == "Selected"
            )

        elif filter_status == "Rejected Candidates":

            query = query.filter(
                Application.status == "Rejected"
            )

        applications = (
            query.order_by(
                Application.resume_score.desc()
            )
            .all()
        )

        if not applications:

            st.info("No candidate applications found.")

            return

        for application in applications:

            job = (
                db.query(Job)
                .filter(Job.id == application.job_id)
                .first()
            )

            with st.expander(
                f"{application.candidate_name} | {job.job_role}"
            ):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.write(
                        f"**Candidate Name:** {application.candidate_name}"
                    )

                    st.write(
                        f"**Email:** {application.email}"
                    )

                    st.write(
                        f"**Phone:** {application.phone}"
                    )

                    st.write(
                        f"**Applied For:** {job.job_role}"
                    )

                    st.write(
                        f"**Education:** {application.education}"
                    )

                    st.write(
                        f"**Experience:** {application.experience}"
                    )

                    st.write(
                        f"**Skills:** {application.skills}"
                    )


                    st.write(
                        f"**GitHub:** {application.github}"
                    )

                    st.write(
                        f"**LinkedIn:** {application.linkedin}"
                    )


                with col2:

                    st.metric(
                        "Resume Score",
                        application.resume_score
                    )

                    if application.status == "Selected":

                        st.success("Selected")

                    else:

                        st.error("Rejected")


    except Exception as e:

        st.error(f"Error : {e}")

    finally:

        db.close()