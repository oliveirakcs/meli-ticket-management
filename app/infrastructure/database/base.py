"""
This module sets up the SQLAlchemy declarative base class used for defining ORM models.

Imports:
    - declarative_base: A factory function from SQLAlchemy that returns a new base class from which all mapped classes should inherit.

Attributes:
    - Base: The declarative base class used as a foundation for all ORM model classes. 
      It provides the metadata needed for SQLAlchemy to map Python classes to database tables.

Usage:
    The `Base` class is used as a base for all model classes that define the schema 
    of the application's database. Each model class should inherit from `Base` 
    to be recognized by SQLAlchemy.

    This setup allows SQLAlchemy to handle the conversion between database rows 
    and Python objects, enabling ORM functionalities such as querying and persisting data.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
