"""
This module provides controllers for managing users, tickets. severity, categories and subcategories.
"""

from .users_controller import UserController, get_user_controller
from .ticket_controller import TicketController, get_ticket_controller
from .severity_controller import SeverityController, get_severity_controller
from .category_controller import CategoryController, get_category_controller
from .subcategory_controller import SubcategoryController, get_subcategory_controller
