"""
Authentication Schemas

This module defines the Pydantic models used for handling authentication
within the application. These models include schemas for login credentials,
authentication tokens, and the data contained within those tokens.

Classes:
    Login: Represents the login credentials required for authentication.
    Token: Represents the authentication token issued upon successful login.
    TokenData: Represents the data stored within the authentication token,
        including user ID, username, role, and scopes/permissions.
"""

import uuid
from typing import List, Optional, Union
from pydantic import BaseModel


class Login(BaseModel):
    """
    Model representing the login credentials.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username: str
    password: str

    class Config:
        """
        Configuration for the model.

        This class defines additional settings and configurations for the Pydantic model.
        """

        from_attributes = True


class Token(BaseModel):
    """
    Model representing the authentication token.

    Attributes:
        access_token (str): The access token for authentication.
        token_type (str): The type of the token (e.g., "bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model representing the data stored in the authentication token.

    Attributes:
        id (Optional[Union[int, uuid.UUID]]): The unique identifier of the user.
        username (Optional[str]): The username of the user.
        role (Optional[str]): The role of the user.
        scopes (List[str]): The list of scopes/permissions associated with the token.
    """

    id: Optional[Union[int, uuid.UUID]]
    username: Optional[str]
    role: Optional[str]
    scopes: List[str] = []
