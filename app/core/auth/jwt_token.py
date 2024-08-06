"""JWT Token related functions"""

from typing import List
import uuid
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas.auth import TokenData

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict, scopes: List[str] = None):
    """
    Create access token.

    Creates a JWT access token based on the provided data and scopes.

    Parameters:
    - data (dict): The data to encode into the access token.
    - scopes (List[str], optional): The list of scopes to include in the token. Defaults to None.

    Returns:
    - str: The JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "scopes": scopes or []})
    to_encode["id"] = str(to_encode["id"])
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify token.

    Verifies the provided JWT token and extracts the username, user ID, role, and scopes.

    Parameters:
    - token (str): The JWT token to verify.
    - credentials_exception: The exception to raise if verification fails.

    Returns:
    - schemas.TokenData: The token data containing the username, user ID, role, and scopes.

    Raises:
    - credentials_exception: If there's an issue decoding the token or if the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("id")
        role: str = payload.get("role")
        scopes: List[str] = payload.get("scopes", [])
        if not username or not user_id or not role:
            raise credentials_exception
        user_id_uuid = uuid.UUID(user_id)
        token_data = TokenData(username=username, id=user_id_uuid, role=role, scopes=scopes)
        return token_data
    except JWTError:
        raise credentials_exception from credentials_exception
