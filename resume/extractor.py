"""
extractor.py
-----------------------------------------
Advanced Resume Extractor
Compatible with existing project
"""

import re

# -----------------------------------------------------
# Skill Database
# -----------------------------------------------------

SKILLS = {

    # Programming Languages
    "Python","Java","C","C++","C#","JavaScript","TypeScript",
    "PHP","Go","Kotlin","Swift","R","MATLAB",

    # Web Technologies
    "HTML","HTML5","CSS","CSS3","Bootstrap","Tailwind CSS",
    "React","ReactJS","Angular","Vue","Next.js","Node.js",
    "Express","Express.js","Django","Flask","FastAPI",
    "Spring","Spring Boot","Hibernate",

    # Mobile Development
    "Flutter","Android","Android Studio","React Native",

    # Databases
    "SQL","MySQL","PostgreSQL","MongoDB","SQLite",
    "Oracle","SQL Server","Firebase","Redis",

    # AI / ML / Data Science
    "Machine Learning","Deep Learning","Artificial Intelligence",
    "AI","Gen AI","Generative AI","LLM","NLP",
    "Computer Vision","OpenCV","TensorFlow","PyTorch",
    "Scikit-learn","Pandas","NumPy","Matplotlib",
    "Seaborn","Data Analysis","Data Visualization",
    "Power BI","Tableau","Excel",

    # Automation & Testing
    "Selenium","Playwright","PW","Cypress","JUnit",
    "PyTest","JMeter","Postman","REST API","API Testing",

    # DevOps / Cloud
    "Git","GitHub","GitLab","Bitbucket",
    "Docker","Kubernetes","CI/CD","Jenkins",
    "AWS","Azure","GCP","Linux",

    # IDE / Tools
    "VSCode","Visual Studio Code","Visual Studio",
    "Eclipse","IntelliJ IDEA","PyCharm",
    "Figma","Jira","Salesforce CRM",

    # Concepts
    "OOP","DSA","Operating System","DBMS",
    "Computer Networks","Networking",

    # Resume Skills
    "Problem Solving","Strategic Solving",
    "Critical Thinking","Communication",
    "Leadership","Teamwork","Time Management",
    "Analytical Skills","Product Debugging",
    "POC Execution","Pre-Sales Consulting",
    "Post-Sales Consulting","BFSI",

    # Others
    "GitHub Actions","Microservices",
    "Streamlit","Apache Spark","Hadoop",
    "Power Automate","Power Apps"

}


# -----------------------------------------------------
# Common Section Headings
# -----------------------------------------------------

SECTION_HEADINGS = {

    "education":[

        "education",

        "academic",

        "academic qualification",

        "qualification",

        "academics"

    ],

    "experience":[

        "experience",

        "work experience",

        "professional experience",

        "employment",

        "internship"

    ],

    "projects":[

        "projects",

        "project",

        "academic projects",

        "personal projects"

    ],

    "skills":[

        "skills",

        "technical skills",

        "core skills",

        "technical expertise",

        "competencies"

    ],

    "certifications":[

        "certification",

        "certifications",

        "courses"

    ], 
        "portfolio": [
        "portfolio",
        "personal website",
        "website"
    ]

}


# -----------------------------------------------------
# Clean Text
# -----------------------------------------------------

def clean_text(text):

    text = text.replace("\t"," ")

    text = re.sub(r"\r","\n",text)

    text = re.sub(r"\n{2,}","\n",text)

    text = re.sub(r"[ ]{2,}"," ",text)

    return text.strip()


# -----------------------------------------------------
# Find Section Positions
# -----------------------------------------------------

def find_sections(text):

    sections={}

    lower=text.lower()

    for key,values in SECTION_HEADINGS.items():

        for heading in values:

            pattern=rf"(^|\n)\s*{re.escape(heading)}\s*:?"

            match=re.search(pattern,lower)

            if match:

                sections[key]=match.start()

                break

    return dict(sorted(sections.items(),key=lambda x:x[1]))


# -----------------------------------------------------
# Extract Text Between Sections
# -----------------------------------------------------

def get_section(text,section_name):

    sections=find_sections(text)

    if section_name not in sections:

        return ""

    names=list(sections.keys())

    index=names.index(section_name)

    start=sections[section_name]

    if index==len(names)-1:

        end=len(text)

    else:

        end=sections[names[index+1]]

    value=text[start:end]

    value=value.split("\n",1)

    if len(value)>1:

        value=value[1]

    else:

        value=value[0]

    value=value.strip()

    value=re.sub(r"\n{2,}","\n",value)

    return value

# -----------------------------------------------------
# Name
# -----------------------------------------------------

def extract_name(text):

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:8]:

        if (
            "@" not in line
            and len(line.split()) >= 2
            and len(line) < 40
            and not any(ch.isdigit() for ch in line)
        ):
            return line.title()

    return "Not Found"


# -----------------------------------------------------
# Email
# -----------------------------------------------------

def extract_email(text):

    match = re.search(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text

    )

    if match:

        return match.group()

    return "Not Found"


# -----------------------------------------------------
# Phone
# -----------------------------------------------------

def extract_phone(text):

    match = re.search(

        r"(\+91[\-\s]?)?[6-9]\d{9}",

        text

    )

    if match:

        return match.group()

    return "Not Found"


# -----------------------------------------------------
# Education
# -----------------------------------------------------

def extract_education(text):

    education = get_section(text, "education")

    if education:

        education = re.sub(r"\n+", "\n", education)

        return education.strip()

    degrees = [

        "Bachelor",

        "Master",

        "BCA",

        "MCA",

        "B.Tech",

        "BE",

        "B.Sc",

        "M.Sc",

        "Diploma",

        "HSC",

        "SSC"

    ]

    lines = text.split("\n")

    result = []

    for line in lines:

        for degree in degrees:

            if degree.lower() in line.lower():

                result.append(line.strip())

                break

    if result:

        return "\n".join(result)

    return "Not Mentioned"


# -----------------------------------------------------
# Experience
# -----------------------------------------------------

def extract_experience(text):

    experience = get_section(text, "experience")

    if not experience:
        return "Fresher"

    stop_words = [
        "education",
        "projects",
        "skills",
        "certifications",
        "languages",
        "achievements"
    ]

    lines = []

    for line in experience.split("\n"):

        l = line.strip()

        if not l:
            continue

        if any(l.lower().startswith(word) for word in stop_words):
            break

        lines.append(l)

    experience = "\n".join(lines).strip()

    if len(experience) < 15:
        return "Fresher"

    return experience

# -----------------------------------------------------
# Skills
# -----------------------------------------------------

# -----------------------------------------------------
# Skills
# -----------------------------------------------------

def extract_skills(text):

    skills_section = get_section(text, "skills")

    source = skills_section if skills_section else text
    source = source.lower()

    found = []

    for skill in SKILLS:

        skill_lower = skill.lower()

        # Handle skills with special characters
        if any(ch in skill_lower for ch in ["/", ".", "+", "#", "-"]):

            if skill_lower in source:
                found.append(skill)

        else:

            pattern = r"\b" + re.escape(skill_lower) + r"\b"

            if re.search(pattern, source):
                found.append(skill)

    found = sorted(set(found))

    if not found:
        return "Not Mentioned"

    return ", ".join(found)
# -----------------------------------------------------
# Projects
# -----------------------------------------------------

def extract_projects(text):

    projects = get_section(text, "projects")

    if not projects:

        return "Not Mentioned"

    
    # Stop if another heading accidentally enters
    stop_words = [

        "education",
        "skills",
        "certification",
        "experience",
        "languages",
        "achievements",
        "interests",
        "contact",
        "profile",
        "summary",
        "objective"

    ]

    lines = []

    for line in projects.split("\n"):

        l = line.strip()

        if not l:
            continue

        if l.lower() in stop_words:
            break

        lines.append(l)

    return "\n".join(lines).strip()


# -----------------------------------------------------
# GitHub
# -----------------------------------------------------

def extract_github(text):

    match = re.search(

        r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+",

        text,

        re.I

    )

    if match:

        return match.group()

    return "Not Mentioned"


# -----------------------------------------------------
# LinkedIn
# -----------------------------------------------------

def extract_linkedin(text):

    match = re.search(

        r"https?://(?:www\.)?linkedin\.com/[^\s]+",

        text,

        re.I

    )

    if match:

        return match.group()

    return "Not Mentioned"


# -----------------------------------------------------
# Portfolio
# -----------------------------------------------------

# -----------------------------------------------------
# Portfolio
# -----------------------------------------------------

def extract_portfolio(text):

    portfolio = get_section(text, "portfolio")

    if portfolio:

        urls = re.findall(r"https?://[^\s]+", portfolio)

        if urls:

            return urls[0]

    return "Not Mentioned"


# -----------------------------------------------------
# Main Function
# -----------------------------------------------------

def extract_details(text):

    text = clean_text(text)

    data = {}

    data["name"] = extract_name(text)

    data["email"] = extract_email(text)

    data["phone"] = extract_phone(text)

    data["education"] = extract_education(text)

    data["experience"] = extract_experience(text)

    data["skills"] = extract_skills(text)

    data["projects"] = extract_projects(text)

    data["github"] = extract_github(text)

    data["linkedin"] = extract_linkedin(text)

    data["portfolio"] = extract_portfolio(text)

    return data