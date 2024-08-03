"""Auth Routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.infrastructure.database.models import User
from app.infrastructure.database import get_db
from app.core.auth.hashing import Hash
from app.core.auth.jwt_token import create_access_token
from app.core import ROLE_SCOPES

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and generate access token.

    This endpoint is used to authenticate users by validating their credentials
    (username and password). If the credentials are valid, an access token is generated
    and returned to the client.

    Args:
        request (OAuth2PasswordRequestForm): The request containing user credentials.
            Defaults to Depends().
        db (Session): The database session dependency. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the generated access token and token type.

    Raises:
        HTTPException: If the provided credentials are invalid or incorrect.
    """

    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    scopes = ROLE_SCOPES.get(user.role, [])
    access_token = create_access_token(data={"id": user.id, "username": user.username, "role": user.role}, scopes=scopes)

    data = {"access_token": access_token, "user_id": user.id, "role": user.role, "scopes": scopes, "token_type": "bearer"}

    return data
