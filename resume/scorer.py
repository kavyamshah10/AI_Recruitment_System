"""
scorer.py
------------------------------------
Improved Resume Scoring System
"""

import re


# ==========================================
# Skills Score (40 Marks)
# ==========================================

def calculate_skills_score(candidate_skills, required_skills):

    candidate = {
        skill.strip().lower()
        for skill in candidate_skills.split(",")
        if skill.strip()
    }

    required = {
        skill.strip().lower()
        for skill in required_skills.split(",")
        if skill.strip()
    }

    if not required:
        return 0

    matched = len(candidate.intersection(required))

    return round((matched / len(required)) * 40)


# ==========================================
# Project Score (25 Marks)
# ==========================================

def calculate_project_score(projects):

    if not projects or projects == "Not Mentioned":
        return 0

    score = 0

    # Count project titles
    total_projects = len(
        re.findall(
            r"(project\s*\d+|^\d+\.)",
            projects,
            re.I | re.M
        )
    )

    if total_projects == 0:
        total_projects = 1

    score += min(total_projects * 8, 16)

    github = len(
        re.findall(
            r"github",
            projects,
            re.I
        )
    )

    live = len(
        re.findall(
            r"live app|streamlit|render|vercel|netlify",
            projects,
            re.I
        )
    )

    score += min(github * 3, 6)

    score += min(live * 3, 6)

    return min(score, 25)


# ==========================================
# Education Score (10 Marks)
# ==========================================

def calculate_education_score(education):

    if education and education != "Not Mentioned":

        return 10

    return 0


# ==========================================
# GitHub Score (5 Marks)
# ==========================================

def calculate_github_score(github):

    if github and github != "Not Mentioned":

        return 5

    return 0


# ==========================================
# LinkedIn Score (5 Marks)
# ==========================================

def calculate_linkedin_score(linkedin):

    if linkedin and linkedin != "Not Mentioned":

        return 5

    return 0


# ==========================================
# Resume Quality (10 Marks)
# ==========================================

def calculate_resume_quality(details):

    score = 0

    fields = [

        details["name"],
        details["email"],
        details["phone"],
        details["education"],
        details["skills"],
        details["projects"]

    ]

    for field in fields:

        if field not in ["", None, "Not Found", "Not Mentioned"]:

            score += 2

    return min(score, 10)


# ==========================================
# Experience Bonus (5 Marks)
# ==========================================

def calculate_experience_bonus(experience):

    if not experience:

        return 0

    exp = experience.lower()

    if exp == "fresher":

        return 0

    if "intern" in exp:

        return 2

    if "1 year" in exp or "2 year" in exp:

        return 3

    if "3 year" in exp or "4 year" in exp:

        return 4

    if "5 year" in exp or "6 year" in exp:

        return 5

    return 2


# ==========================================
# Total Score
# ==========================================

def calculate_resume_score(details, job):

    skills = calculate_skills_score(
        details["skills"],
        job.required_skills
    )

    projects = calculate_project_score(
        details["projects"]
    )

    education = calculate_education_score(
        details["education"]
    )

    github = calculate_github_score(
        details["github"]
    )

    linkedin = calculate_linkedin_score(
        details["linkedin"]
    )

    quality = calculate_resume_quality(
        details
    )

    experience = calculate_experience_bonus(
        details["experience"]
    )

    total = (
        skills
        + projects
        + education
        + github
        + linkedin
        + quality
        + experience
    )

    return min(total, 100)


# ==========================================
# Selection Status
# ==========================================

def get_status(score, minimum_score):

    if score >= minimum_score:

        return "Selected"

    return "Rejected"