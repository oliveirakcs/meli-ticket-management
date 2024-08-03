"""OAuth2 decoding JWT Token related functions."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from app import schemas
from . import jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded user information.

    Raises:
        HTTPException: If credentials cannot be validated.

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return jwt_token.verify_token(token, credentials_exception)


def get_current_active_user(security_scopes: SecurityScopes, current_user: schemas.User = Depends(get_current_user)):
    """
    Verify that the current user has the necessary scopes.

    Args:
        security_scopes (SecurityScopes): The security scopes required.
        current_user (schemas.User): The current user extracted from the token.

    Returns:
        schemas.User: The current user.

    Raises:
        HTTPException: If the user does not have the necessary permissions.
    """
    if security_scopes.scopes:
        token_scopes = current_user.scopes
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                )
    return current_user
