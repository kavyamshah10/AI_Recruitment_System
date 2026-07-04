"""
manage_jobs.py
-----------------------------------------
View and Manage Posted Jobs
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Job


def manage_jobs_page():

    st.subheader("Manage Jobs")

    db = SessionLocal()

    try:

        jobs = (
            db.query(Job)
            .order_by(Job.id.desc())
            .all()
        )

        if not jobs:

            st.info("No jobs posted yet.")

            return

        for job in jobs:

            with st.container():

                st.markdown("---")

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.write(f"### {job.job_role}")

                    st.write(
                        f"**Required Skills:** {job.required_skills}"
                    )

                    st.write(
                        f"**Minimum Score:** {job.minimum_score}"
                    )

                    st.write(
                        f"**Posted By:** {job.posted_by}"
                    )

                    st.write(
                        f"**Applications Received:** {job.total_applications}"
                    )

                    if job.is_open:

                        st.success("Status : Open")

                    else:

                        st.error("Status : Closed")

                with col2:

                    if job.is_open:

                        if st.button(
                            "Close Job",
                            key=f"close_{job.id}"
                        ):

                            job.is_open = False

                            db.commit()

                            st.success(
                                "Job Closed Successfully."
                            )

                            st.rerun()

                    else:

                        st.button(
                            "Closed",
                            disabled=True,
                            key=f"closed_{job.id}"
                        )

    except Exception as e:

        st.error(f"Error : {e}")

    finally:

        db.close()