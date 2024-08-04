"""
Module containing enumerations used across the application.

This module provides enumerations to represent various constants and choices
that are used throughout the application. Enumerations help in improving code
readability, maintainability, and also provide validation out of the box.

Classes:
    DwRecordStatus: Enumeration to represent the archived status of Data Warehouses.
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
