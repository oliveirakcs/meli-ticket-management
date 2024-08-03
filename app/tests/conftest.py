"""
Global fixtures for API testing.
"""

from dotenv import load_dotenv, find_dotenv
import pytest
from app.tests import create_client

load_dotenv(find_dotenv(".env"))
client = create_client()


@pytest.fixture(name="user", scope="session")
def create_user(access_token, company):
    """
    Fixture to create a user.

    Args:
        access_token (str): Access token for authorization.

    Returns:
        dict: Data of the created user.
    """
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "company_id": company["id"],
            "role": "sysadmin",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    return response.json()
