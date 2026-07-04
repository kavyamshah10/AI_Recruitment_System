import requests
import streamlit as st
from database.database import SessionLocal
from database.models import Candidate


def view_resume(candidate_id):

    st.subheader("Candidate Resume")

    db = SessionLocal()

    try:

        candidate = (
            db.query(Candidate)
            .filter(Candidate.id == candidate_id)
            .first()
        )

        if candidate is None:
            st.error("Candidate not found.")
            return

        if not candidate.resume_path:
            st.warning("Resume not uploaded.")
            return

        st.write(f"**Resume File:** {candidate.resume_name}")

        # ✅ DOWNLOAD ONLY (NO VIEW)
        pdf_data = requests.get(candidate.resume_path).content

        st.download_button(
            label="📄 Download Resume",
            data=pdf_data,
            file_name=candidate.resume_name or "resume.pdf",
            mime="application/pdf"
        )

        st.success("Click above to download resume")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        db.close()