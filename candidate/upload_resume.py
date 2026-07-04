"""
upload_resume.py
------------------------------------------
Upload Resume and start AI processing.
"""

import streamlit as st

from database.database import SessionLocal
from database.models import Job

from resume.utils import (
    save_resume,
    get_resume_text
)

from utils.validators import validate_resume
from resume.extractor import extract_details
from resume.scorer import (
    calculate_resume_score,
    get_status
)
from resume.matcher import (
    match_resume,
    get_recommendation
)

from database.models import Candidate, Application


def upload_resume_page():

    st.subheader("Upload Resume")

    # -----------------------------
    # Check Job Selection
    # -----------------------------

    if "apply_job" not in st.session_state:

        st.warning(
            "Please apply for a job first."
        )

        return

    job_id = st.session_state.apply_job

    db = SessionLocal()

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:

        st.error("Selected job not found.")

        db.close()

        return

    # -----------------------------
    # Job Information
    # -----------------------------

    st.write(f"### Applying For")

    st.info(f"{job.job_role}")

    st.write(
        f"**Required Skills:** {job.required_skills}"
    )

    st.write(
        f"**Minimum Score:** {job.minimum_score}"
    )

    st.markdown("---")

    # -----------------------------
    # Resume Upload
    # -----------------------------
    candidate = (
    db.query(Candidate)
        .filter(Candidate.user_id == st.session_state.user_id)
        .first()
    )

    if candidate and candidate.resume_path:
        st.success("✅ Resume already uploaded and processed.")
        st.write("You can view your Score and Status without uploading again.")
        db.close()
        return
    uploaded_file = st.file_uploader(

        "Upload Resume",

        type=["pdf", "docx"]

    )

    if uploaded_file is None:

        db.close()

        return

    # -----------------------------
    # Validate Resume
    # -----------------------------

    valid, message = validate_resume(
        uploaded_file
    )

    if not valid:

        st.error(message)

        db.close()

        return

    # -----------------------------
    # Save Resume
    # -----------------------------
    resume_name, resume_path = save_resume(
        uploaded_file,
        "uploads/resumes"
    )

    st.session_state.resume_name = resume_name
    st.session_state.resume_path = resume_path



    st.success("Resume uploaded successfully.")
    

    st.write(f"**File:** {resume_name}")

    st.markdown("---")

    # -----------------------------
    # Start Processing
    # -----------------------------

    if st.button("Process Resume"):

        with st.spinner(
            "Processing Resume..."
        ):

            resume_text = get_resume_text(
                resume_path
            )

            if len(resume_text.strip()) == 0:

                st.error(
                    "Unable to extract text from resume."
                )

                db.close()

                return

            # Pass data to Part 2
            st.session_state.resume_text = resume_text
            st.session_state.resume_name = resume_name

            details = extract_details(resume_text)
            resume_score = calculate_resume_score(
                details,
                job
            )

            status = get_status(
               resume_score,
               job.minimum_score
            )

            match_result = match_resume(
               details["skills"],
               job.required_skills
            )

            recommendation = get_recommendation(
                match_result["match_percentage"]
            )

            st.session_state.resume_path = resume_path

            st.session_state.resume_details = details

            st.session_state.resume_score = resume_score

            st.session_state.application_status = status

            st.session_state.match_result = match_result

            st.session_state.recommendation = recommendation

            st.session_state.resume_name = resume_name

            st.success("Resume processed successfully.")

            st.markdown("---")

            st.subheader("Extracted Details")

            st.write(f"**Name:** {details['name']}")

            st.write(f"**Email:** {details['email']}")

            st.write(f"**Phone:** {details['phone']}")

            st.write(f"**Education:** {details['education']}")

            st.write(f"**Experience:** {details['experience']}")

            st.write(f"**Skills:** {details['skills']}")

            st.write(f"**Projects:** {details['projects']}")

            st.write(f"**GitHub:** {details['github']}")
            
            st.write(f"**LinkedIn:** {details['linkedin']}")

            st.write(f"**Portfolio:** {details['portfolio']}")

            st.markdown("---")

            st.subheader("Resume Analysis")

            st.success(
                "Resume parsed successfully."
            )

            st.metric(
              "Resume Score",
              f"{resume_score}/100"
            )

            st.metric(
              "Skill Match",
               f"{match_result['match_percentage']}%"
            )

            st.write(
               f"**Recommendation:** {recommendation}"
            )

            if status == "Selected":
                st.success(

                  f"Application Status : {status}"
                )
            
            else:

                st.error(
                  f"Application Status : {status}"
                )

            st.markdown("---")



            if True:

                details = st.session_state.resume_details

                score = st.session_state.resume_score

                status = st.session_state.application_status

                candidate = (
                   db.query(Candidate)
                   .filter(
                   Candidate.user_id == st.session_state.user_id
                   )
                   .first()
                )

                if candidate is None:

                    candidate = Candidate(

                        user_id=st.session_state.user_id,

                        phone=details["phone"],

                        education=details["education"],

                        experience=details["experience"],

                        skills=details["skills"],

                        github=details["github"],

                        linkedin=details["linkedin"],

                        resume_name=st.session_state.resume_name,

                        resume_path=resume_path,

                        resume_score=score

                    )

                    db.add(candidate)

                    db.flush()

                else:

                    candidate.phone = details["phone"]

                    candidate.education = details["education"]

                    candidate.experience = details["experience"]

                    candidate.skills = details["skills"]

                    candidate.github = details["github"]

                    candidate.linkedin = details["linkedin"]

                    candidate.resume_name = st.session_state.resume_name

                    candidate.resume_path =resume_path

                    candidate.resume_score = score

                    db.flush()

    # -----------------------------
    # Application Table
    # -----------------------------
                existing_application = (
                    db.query(Application)
                    .filter(
                        Application.user_id == st.session_state.user_id,
                        Application.job_id == job.id
                    )
                    .first()
                )

                if existing_application is None:

                    application = Application(

                        user_id=st.session_state.user_id,

                        candidate_id=candidate.id,

                        job_id=job.id,

                        candidate_name=details["name"],

                        email=details["email"],

                        phone=details["phone"],

                        education=details["education"],

                        experience=details["experience"],

                        skills=details["skills"],

                        github=details["github"],

                        linkedin=details["linkedin"],

                        resume_score=score,

                        status=status

                    )
                    db.add(application)
                    job.total_applications += 1
                else:

                    existing_application.candidate_name = details["name"]
                    existing_application.email = details["email"]
                    existing_application.phone = details["phone"]
                    existing_application.education = details["education"]
                    existing_application.experience = details["experience"]
                    existing_application.skills = details["skills"]
                    existing_application.github = details["github"]
                    existing_application.linkedin = details["linkedin"]
                    existing_application.resume_score = score
                    existing_application.status = status                

                db.commit()

                
                st.write(f"**Experience Required:** {job.experience}")

                st.write(f"**Salary:** {job.salary}")

                st.write(f"**Location:** {job.location}")

                st.write(f"### Resume Score : {score}/100")

                st.write(f"### Status : {status}")

                st.success("Application Submitted Successfully!")

                st.balloons()

    db.close()
