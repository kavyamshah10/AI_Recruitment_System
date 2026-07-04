"""
matcher.py
------------------------------------
Matches candidate skills with
job required skills.
"""


# ==========================================
# Match Resume with Job
# ==========================================

def match_resume(candidate_skills, required_skills):
    """
    Compare candidate skills with
    required job skills.
    """

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

    matched_skills = sorted(candidate.intersection(required))

    missing_skills = sorted(required - candidate)

    if len(required) == 0:
        match_percentage = 0
    else:
        match_percentage = round(
            (len(matched_skills) / len(required)) * 100,
            2
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }


# ==========================================
# Recommendation
# ==========================================

def get_recommendation(match_percentage):
    """
    AI recommendation based on
    skill match percentage.
    """

    if match_percentage >= 80:
        return "Excellent Match"

    elif match_percentage >= 60:
        return "Good Match"

    elif match_percentage >= 40:
        return "Average Match"

    return "Poor Match"