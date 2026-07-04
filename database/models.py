from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship
from datetime import datetime

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False, unique=True)

    email = Column(String(150), nullable=False, unique=True)

    password_hash = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship(
        "Candidate",
        back_populates="user",
        uselist=False
    )


# ======================================================
# JOBS TABLE
# ======================================================

class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    job_role = Column(String(150), nullable=False)

    job_description = Column(Text, nullable=False)

    required_skills = Column(Text, nullable=False)

    experience = Column(String(100))

    salary = Column(String(100))

    location = Column(String(100))

    posted_by = Column(String(100))

    minimum_score = Column(Integer, nullable=False)

    total_applications = Column(Integer, default=0)

    status = Column(String(20), default="Open")

    created_at = Column(DateTime, default=datetime.utcnow)

    is_open = Column(Boolean, default=True)

    applications = relationship(
        "Application",
        back_populates="job"
    )


# ======================================================
# CANDIDATES TABLE
# ======================================================

class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    phone = Column(String(20))

    education = Column(Text)

    experience = Column(Text)

    skills = Column(Text)

    github = Column(String(255))

    linkedin = Column(String(255))

    resume_name = Column(String(255))

    resume_path = Column(String(255))

    resume_score = Column(Integer)

    user = relationship(
        "User",
        back_populates="candidate"
    )

    applications = relationship(
        "Application",
        back_populates="candidate"
    )


# ======================================================
# APPLICATIONS TABLE
# ======================================================

class Application(Base):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id")
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id")
    )

    candidate_name = Column(String(100))

    email = Column(String(150))

    phone = Column(String(20))

    education = Column(Text)

    experience = Column(Text)

    skills = Column(Text)

    github = Column(String(255))

    linkedin = Column(String(255))

    resume_score = Column(Integer)

    status = Column(String(30), default="Rejected")

    applied_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    candidate = relationship(
        "Candidate",
        back_populates="applications"
    )

    job = relationship(
        "Job",
        back_populates="applications"
    )