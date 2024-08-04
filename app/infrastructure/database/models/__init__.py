"""
This module imports ORM models used for database interactions in the application.

The following models are imported:

- **Severity**: Represents the severity levels associated with different tickets. 
  Used to categorize and prioritize issues or requests based on their importance or urgency.

- **Ticket**: Defines the structure of a ticket entity within the application. 
  Tickets are used to track issues, requests, or tasks, containing details like 
  title, description, associated user, and status.

- **Category**: Represents a high-level grouping for tickets, allowing for 
  categorization and organization of tickets into broader topics or areas.

- **Subcategory**: Provides a more granular categorization within a category. 
  Subcategories help in further detailing the classification of tickets under a 
  specific category.

- **User**: Defines the user entity, which includes information such as user 
  credentials, profile details, and permissions. Users are associated with tickets 
  and can be assigned roles and responsibilities.

Usage:
    These models are used throughout the application to create, read, update, and 
    delete records from the database. They serve as the blueprint for the database 
    tables and allow SQLAlchemy to map Python objects to rows in the database.

Note:
    Ensure that database connections and sessions are properly set up when working 
    with these models. They require an active database session to execute operations.
"""

from app.infrastructure.database.models.severity import Severity
from app.infrastructure.database.models.ticket import Ticket
from app.infrastructure.database.models.category import Category
from app.infrastructure.database.models.subcategory import Subcategory
from app.infrastructure.database.models.user import User
from app.infrastructure.database.models.ticket_category import TicketCategory
from app.infrastructure.database.models.ticket_subcategory import TicketSubcategory
