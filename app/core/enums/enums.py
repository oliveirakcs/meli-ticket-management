"""
Module containing enumerations used across the application.


"""

from enum import Enum


class TicketStatus(str, Enum):
    """
    Enumeration to represent the status of Tickets.

    Attributes:
        ABERTO: Represents an open ticket.
        EM_PROGRESSO: Represents a ticket that is in progress.
        RESOLVIDO: Represents a resolved ticket.
    """

    ABERTO = "aberto"
    EM_PROGRESSO = "em progresso"
    RESOLVIDO = "resolvido"
