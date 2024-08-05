"""
Unit tests for fetching random comment data from the JSONPlaceholder API.
"""

import unittest
import requests_mock
from fastapi import HTTPException
from app.scripts import External


class TestExternalComment(unittest.TestCase):
    """
    Class for unit tests for fetching random comment data from the JSONPlaceholder API.
    """

    def setUp(self):
        """
        Setup for the tests.
        """
        self.comment_url = "https://jsonplaceholder.typicode.com/comments"

    @requests_mock.Mocker()
    def test_fetch_random_comment_success(self, mock_request):
        """
        Test fetch_random_comment for successful response.
        """
        mock_data = [
            {"postId": 1, "id": 1, "name": "John Doe", "email": "john@example.com", "body": "This is a comment."},
            {"postId": 1, "id": 2, "name": "Jane Doe", "email": "jane@example.com", "body": "Another comment here."},
        ]

        mock_request.get(self.comment_url, json=mock_data)

        result = External.fetch_random_comment()

        self.assertIn("comment_text", result)
        self.assertIn("comment_user", result)
        self.assertIn(result["comment_user"], ["john@example.com", "jane@example.com"])
        self.assertTrue(isinstance(result["comment_text"], str))
        self.assertTrue(isinstance(result["comment_user"], str))

    @requests_mock.Mocker()
    def test_fetch_random_comment_http_error(self, mock_request):
        """
        Test fetch_random_comment when an HTTP error occurs.
        """
        mock_request.get(self.comment_url, status_code=500)

        with self.assertRaises(HTTPException) as context:
            External.fetch_random_comment()

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.detail, "Error fetching comments from external API")

    def test_fetch_random_comment_actual_request(self):
        """
        Test fetch_random_comment with an actual API request.
        """
        try:
            result = External.fetch_random_comment()
            self.assertIn("comment_text", result)
            self.assertIn("comment_user", result)
            self.assertTrue(isinstance(result["comment_text"], str))
            self.assertTrue(isinstance(result["comment_user"], str))
        except HTTPException as e:
            self.fail(f"HTTPException raised unexpectedly: {e.detail}")
