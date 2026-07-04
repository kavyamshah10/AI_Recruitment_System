"""
hr_chatbot.py
-----------------------------------------
Smart HR AI Chatbot
"""

import re

from sqlalchemy import func

from database.database import SessionLocal
from database.models import Application, Job


def format_candidate(candidate, job):

    return (
        f"• {candidate.candidate_name}\n"
        f"Job : {job.job_role}\n"
        f"Score : {candidate.resume_score}\n"
        f"Status : {candidate.status}\n"
        f"Email : {candidate.email}\n\n"
    )


def get_chatbot_response(question):

    db = SessionLocal()

    try:

        query = question.lower().strip()

        # ======================================
        # Total Applications
        # ======================================

        if any(x in query for x in [
            "total candidate",
            "total candidates",
            "how many candidate",
            "how many candidates",
            "applications"
        ]):

            total = db.query(Application).count()

            return f"Total Applications : {total}"

        # ======================================
        # Selected Count
        # ======================================

        if "how many selected" in query:

            total = (
                db.query(Application)
                .filter(Application.status == "Selected")
                .count()
            )

            return f"Selected Candidates : {total}"

        # ======================================
        # Rejected Count
        # ======================================

        if "how many rejected" in query:

            total = (
                db.query(Application)
                .filter(Application.status == "Rejected")
                .count()
            )

            return f"Rejected Candidates : {total}"

        # ======================================
        # Selected Candidates
        # ======================================

        if "selected" in query:

            candidates = (
                db.query(Application)
                .filter(Application.status == "Selected")
                .order_by(Application.resume_score.desc())
                .all()
            )

            if not candidates:
                return "No selected candidates found."

            response = "Selected Candidates\n\n"

            for c in candidates:

                job = db.query(Job).filter(Job.id == c.job_id).first()

                response += format_candidate(c, job)

            return response

        # ======================================
        # Rejected Candidates
        # ======================================

        if "rejected" in query:

            candidates = (
                db.query(Application)
                .filter(Application.status == "Rejected")
                .order_by(Application.resume_score.desc())
                .all()
            )

            if not candidates:
                return "No rejected candidates found."

            response = "Rejected Candidates\n\n"

            for c in candidates:

                job = db.query(Job).filter(Job.id == c.job_id).first()

                response += format_candidate(c, job)

            return response

        # ======================================
        # Top Candidates
        # ======================================

        if "top" in query:

            number = 3

            m = re.search(r"\d+", query)

            if m:

                number = int(m.group())

            candidates = (
                db.query(Application)
                .order_by(Application.resume_score.desc())
                .limit(number)
                .all()
            )

            if not candidates:
                return "No candidates found."

            response = f"Top {number} Candidates\n\n"

            for c in candidates:

                job = db.query(Job).filter(Job.id == c.job_id).first()

                response += format_candidate(c, job)

            return response

        # ======================================
        # Highest Score
        # ======================================

        if "highest" in query:

            candidate = (
                db.query(Application)
                .order_by(Application.resume_score.desc())
                .first()
            )

            if not candidate:
                return "No candidates."

            return (
                f"Highest Resume Score\n\n"
                f"{candidate.candidate_name}\n"
                f"Score : {candidate.resume_score}"
            )

        # ======================================
        # Average Score
        # ======================================

        if "average" in query:

            avg = db.query(
                func.avg(Application.resume_score)
            ).scalar()

            if avg is None:
                return "No candidates."

            return f"Average Resume Score : {round(avg,2)}"

        # ======================================
        # Score Above
        # ======================================

        if "score" in query or "above" in query:

            m = re.search(r"\d+", query)

            if not m:

                return "Please specify score."

            score = int(m.group())

            candidates = (
                db.query(Application)
                .filter(Application.resume_score >= score)
                .order_by(Application.resume_score.desc())
                .all()
            )

            if not candidates:
                return "No candidates found."

            response = f"Candidates scoring above {score}\n\n"

            for c in candidates:

                job = db.query(Job).filter(Job.id == c.job_id).first()

                response += format_candidate(c, job)

            return response

        # ======================================
        # Job Role Search
        # ======================================

        jobs = db.query(Job).all()

        for job in jobs:

            if job.job_role.lower() in query:

                applications = (
                    db.query(Application)
                    .filter(Application.job_id == job.id)
                    .all()
                )

                if not applications:
                    return "No candidates applied."

                response = f"{job.job_role} Candidates\n\n"

                for c in applications:

                    response += format_candidate(c, job)

                return response

        # ======================================
        # Skill Search
        # ======================================

        stop_words = {

            "show",
            "candidate",
            "candidates",
            "find",
            "who",
            "know",
            "with",
            "having",
            "skill",
            "skills",
            "for"
        }

        words = query.replace(",", " ").split()

        skill = None

        for word in words:

            if word not in stop_words:

                skill = word

                break

        if skill:

            candidates = db.query(Application).all()

            matched = []

            for c in candidates:

                if c.skills and skill.lower() in c.skills.lower():

                    matched.append(c)

            if matched:

                response = f"Candidates with {skill.title()}\n\n"

                for c in matched:

                    job = db.query(Job).filter(Job.id == c.job_id).first()

                    response += format_candidate(c, job)

                return response

        else: 
            
            return f"No candidates found with '{skill.title()}' skill."
        

    except Exception as e:

        return f"Error : {e}"

    finally:

        db.close()