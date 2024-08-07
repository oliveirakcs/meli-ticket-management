"""Hashing class using bcrypt encryption."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    """A class providing methods for hashing and verifying passwords.

    This module provides a Hash class with methods for hashing and verifying passwords
    using bcrypt encryption.

    Example:
        - hashed = Hash.bcrypt("password123")
        - Hash.verify("password123", hashed)
        True
        - Hash.verify("wrongpassword", hashed)
        False

    """

    @staticmethod
    def bcrypt(password: str):
        """Hash a password using bcrypt encryption.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.

        """
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password, hashed_password):
        """Verify if a plain text password matches a hashed password.

        Args:
            plain_password (str): The plain text password.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.

        """
        return pwd_context.verify(plain_password, hashed_password)
