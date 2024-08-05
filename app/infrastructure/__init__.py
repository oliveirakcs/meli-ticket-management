"""
This module is responsible for the database connection and the creation of the database tables.
"""

from app.infrastructure.database import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, get_db
from app.infrastructure.database.models import Category, Severity, Subcategory, Ticket, User, TicketCategory, TicketSubcategory
from app.infrastructure.database.setup import create_sysadmin, create_severities, create_categories, create_subcategories
