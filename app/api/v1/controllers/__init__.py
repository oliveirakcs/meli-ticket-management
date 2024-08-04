"""
This module provides controllers for managing users, tickets. severity, categories and subcategories.

Imports:
    UserController, get_user_controller from users_controller: User management controller and its getter.
    TicketController, get_ticket_controller from ticket_controller: Ticket management controller and its getter.
    SeverityController, get_severity_controller from severity_controller: Severity management controller and its getter.

Classes:
    UserController: Manages user-related operations.
    TicketController: Manages ticket-related operations.
    SeverityController: Manages severity-related operations.

Functions:
    get_user_controller: Returns an instance of UserController.
    get_ticket_controller: Returns an instance of TicketController.
    get_severity_controller: Returns an instance of SeverityController.
"""

from .users_controller import UserController, get_user_controller
from .ticket_controller import TicketController, get_ticket_controller
from .severity_controller import SeverityController, get_severity_controller
