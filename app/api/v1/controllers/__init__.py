"""
This module provides controllers for managing users and tickets.

Imports:
    UserController, get_user_controller from users_controller: User management controller and its getter.
    TicketController, get_ticket_controller from ticket_controller: Ticket management controller and its getter.

Classes:
    UserController: Manages user-related operations.
    TicketController: Manages ticket-related operations.

Functions:
    get_user_controller: Returns an instance of UserController.
    get_ticket_controller: Returns an instance of TicketController.
"""

from .users_controller import UserController, get_user_controller
from .ticket_controller import TicketController, get_ticket_controller
