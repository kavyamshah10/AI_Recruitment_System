from database.database import engine, Base

from database.models import User, Job, Candidate, Application


def create_database():
    """
    Creates all tables defined in models.py.
    """

    Base.metadata.create_all(bind=engine)

    print("=" * 50)
    print("AI Recruitment System Database Created Successfully!")
    print("=" * 50)


if __name__ == "__main__":
    create_database()