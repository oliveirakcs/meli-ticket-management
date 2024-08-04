"""
This module provides access to various controllers for managing users, tickets, severity, categories and subcategories.

Imports:
    UserController, get_user_controller from controllers: User management controller and its getter.
    TicketController, get_ticket_controller from controllers: Ticket management controller and its getter.
    SeverityController, get_severity_controller from controllers: Severity management controller and its getter.

Classes:
    UserController: Manages user-related operations.
    TicketController: Manages ticket-related operations.
    SeverityController: Manages severity-related operations.

Functions:
    get_user_controller: Returns an instance of UserController.
    get_ticket_controller: Returns an instance of TicketController.
    get_severity_controller: Returns an instance of SeverityController.
"""

from .controllers import UserController, get_user_controller, TicketController, get_ticket_controller, SeverityController, get_severity_controller
