"""
Integration tests for fetching comments from JSONPlaceholder API.
"""

import requests
from app.scripts import External


def test_fetch_random_comment():
    """
    Test fetching a random comment from the JSONPlaceholder API.

    Test steps:
    1. Make a request to the JSONPlaceholder comments endpoint.
    2. Select a random comment.
    3. Verify the response structure and content.
    """
    response = requests.get("https://jsonplaceholder.typicode.com/comments", timeout=5)
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0

    comment_data = External.fetch_random_comment()

    assert "comment_text" in comment_data
    assert "comment_user" in comment_data
    assert isinstance(comment_data["comment_text"], str)
    assert isinstance(comment_data["comment_user"], str)

    assert any(comment_data["comment_text"] == c["body"].replace("\n", " ") for c in comments)
    assert any(comment_data["comment_user"] == c["email"] for c in comments)


def test_comment_content():
    """
    Test to verify the specific content of a fetched comment.

    Test steps:
    1. Fetch a comment.
    2. Verify its text and email fields contain expected values.
    """
    comment_data = External.fetch_random_comment()
    assert "\n" not in comment_data["comment_text"]
    assert "@" in comment_data["comment_user"]
    assert "." in comment_data["comment_user"]
