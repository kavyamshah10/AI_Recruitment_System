"""
top_candidates.py
-----------------------------------------
Display Top 3 Candidates
"""

import streamlit as st

from database.database import SessionLocal
from database.models import (
    Application,
    Job
)


def top_candidates_page():

    st.subheader("🏆 Top 3 Candidates")

    db = SessionLocal()

    try:

        candidates = (

            db.query(Application)

            .order_by(
                Application.resume_score.desc()
            )

            .limit(3)

            .all()

        )

        if not candidates:

            st.info("No applications available.")

            return

        rank = 1

        medals = {
            1: "🥇",
            2: "🥈",
            3: "🥉"
        }

        for candidate in candidates:

            job = (

                db.query(Job)

                .filter(
                    Job.id == candidate.job_id
                )

                .first()

            )

            with st.container():

                st.markdown("---")

                st.markdown(
                    f"## {medals[rank]} Rank {rank}"
                )

                st.write(
                    f"**Candidate:** {candidate.candidate_name}"
                )

                st.write(
                    f"**Applied For:** {job.job_role}"
                )

                st.write(
                    f"**Email:** {candidate.email}"
                )

                st.write(
                    f"**Resume Score:** {candidate.resume_score}/100"
                )

                if candidate.status == "Selected":

                    st.success("Selected")

                else:

                    st.error("Rejected")

            rank += 1

    except Exception as e:

        st.error(f"Error : {e}")

    finally:

        db.close()