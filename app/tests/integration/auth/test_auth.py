"""
Integration tests for the login endpoint in the authentication system.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.infrastructure.database.models import User
from app.infrastructure.database import get_db
from app.core.auth.hashing import Hash
from app.scripts import External

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db_session():
    """
    Fixture for setting up a test database session.
    """
    db = next(get_db())
    yield db
    db.rollback()


@pytest.fixture(scope="function")
def test_user(test_db_session: Session):
    """
    Fixture for setting up a test user in the database.

    Args:
        test_db_session (Session): The test database session.

    Returns:
        User: The created test user.
    """
    user_data = External.fetch_random_user()
    hashed_password = Hash.bcrypt("password123")
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        name=user_data["name"],
        password=hashed_password,
        role="user",
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


def test_login_success(test_user):
    """
    Test the login endpoint for successful authentication.

    Args:
        test_user (User): The test user fixture.

    Test steps:
    1. Send a POST request to the login endpoint with valid credentials.
    2. Verify the response status code is 200 (OK).
    3. Check the presence of an access token in the response.
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": test_user.username, "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_username(test_db_session):
    """
    Test the login endpoint with an invalid username.

    Args:
        test_db_session (Session): The test database session.

    Test steps:
    1. Send a POST request to the login endpoint with an invalid username.
    2. Verify the response status code is 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": "invalid_user", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_password(test_user):
    """
    Test the login endpoint with an invalid password.

    Args:
        test_user (User): The test user fixture.

    Test steps:
    1. Send a POST request to the login endpoint with an invalid password.
    2. Verify the response status code is 401 (Unauthorized).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": test_user.username, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect password"


def test_login_empty_credentials():
    """
    Test the login endpoint with empty credentials.

    Test steps:
    1. Send a POST request to the login endpoint with empty credentials.
    2. Verify the response status code is 422 (Unprocessable Entity).
    """
    response = client.post("/api/v1/login/", data={"username": "", "password": ""})
    assert response.status_code == 422


def test_login_without_password(test_user):
    """
    Test the login endpoint without a password.

    Args:
        test_user (User): The test user fixture.

    Test steps:
    1. Send a POST request to the login endpoint without a password.
    2. Verify the response status code is 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": test_user.username, "password": ""},
    )
    assert response.status_code == 422


def test_login_without_username():
    """
    Test the login endpoint without a username.

    Test steps:
    1. Send a POST request to the login endpoint without a username.
    2. Verify the response status code is 422 (Unprocessable Entity).
    """
    response = client.post(
        "/api/v1/login/",
        data={"username": "", "password": "password123"},
    )
    assert response.status_code == 422
