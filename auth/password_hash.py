"""
password_hash.py
------------------------------------
Handles password hashing and verification
for candidate accounts.
"""

import bcrypt


def hash_password(password):


    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password,
    hashed_password
):


    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )