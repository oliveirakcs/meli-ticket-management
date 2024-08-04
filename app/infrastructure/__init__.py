"""
This module is responsible for setting up and managing the database interactions
for the application. It imports necessary configurations and models for database operations.

Imports:
    - DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER: Constants for database connection.
    - get_db: Function to retrieve the database session.
    - Category, Severity, Subcategory, Ticket, User: ORM models for the database tables.
    - create_sysadmin: Function to create a system administrator user.

Usage:
    This module provides the foundational database setup required for the application,
    including the ORM models representing various entities such as Category, Severity, 
    Subcategory, Ticket, and User. It also handles the creation of a system administrator 
    with the `create_sysadmin` function.

Note:
    Ensure that the database configurations (DB_HOST, DB_NAME, etc.) are properly set
    before using this module to avoid connection issues.
"""

from app.infrastructure.database import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, get_db
from app.infrastructure.database.models import Category, Severity, Subcategory, Ticket, User, TicketCategory, TicketSubcategory
from app.infrastructure.database.setup import create_sysadmin, create_severities, create_categories, create_subcategories
