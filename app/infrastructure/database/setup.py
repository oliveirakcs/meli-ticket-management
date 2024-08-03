"""Create initial tables in the database."""

import os
from app.infrastructure.database.models import User
from app.infrastructure.database import SessionLocal
from app.core.auth.hashing import Hash
from app.infrastructure.database import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

db = SessionLocal()

connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

"""This module provides functions to create initial tables and records in the database."""


def create_sysadmin():
    """Create the sysadmin user if it does not exist.

    This function checks if the sysadmin user exists in the database.
    If not, it creates the sysadmin user.
    """

    user = db.query(User).filter(User.username == "sysadmin").first()

    if not user:
        new_user = User(
            username=os.environ["SYSADMIN_USERNAME"],
            name=os.environ["SYSADMIN_NAME"],
            email=os.environ["SYSADMIN_EMAIL"],
            password=Hash.bcrypt(os.environ["SYSADMIN_PASSWORD"]),
            active=True,
            role="sysadmin",
        )
        db.add(new_user)
        db.commit()
        print("Sysadmin user created!")
