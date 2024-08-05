"""
Integration tests for fetching users from JSONPlaceholder API.
"""

import requests
from app.scripts import External


def test_fetch_random_user():
    """
    Test fetching a random user from the JSONPlaceholder API.

    Test steps:
    1. Make a request to the JSONPlaceholder users endpoint.
    2. Select a random user.
    3. Verify the response structure and content.
    """
    response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0

    user_data = External.fetch_random_user()

    assert "name" in user_data
    assert "email" in user_data
    assert "username" in user_data
    assert isinstance(user_data["name"], str)
    assert isinstance(user_data["email"], str)
    assert isinstance(user_data["username"], str)

    assert any(user_data["name"] == u["name"] for u in users)
    assert any(user_data["email"] == u["email"] for u in users)
    assert any(user_data["username"] == u["username"] for u in users)


def test_user_email_format():
    """
    Test to verify the format of the email of a fetched user.

    Test steps:
    1. Fetch a user.
    2. Verify its email field is in the expected format.
    """
    user_data = External.fetch_random_user()
    assert "@" in user_data["email"]
    assert "." in user_data["email"]
