"""Database Controller"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(connection_string, pool_size=20, max_overflow=10)

SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def get_db():
    """Function to obtain a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
