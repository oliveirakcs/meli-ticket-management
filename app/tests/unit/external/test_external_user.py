"""
Unit tests for fetching random user data from the JSONPlaceholder API.
"""

import unittest
import requests_mock
from fastapi import HTTPException
from app.scripts import External


class TestExternalUser(unittest.TestCase):
    """
    Class for unit tests for fetching random user data from the JSONPlaceholder API.
    """

    def setUp(self):
        """
        Setup for the tests.
        """
        self.user_url = "https://jsonplaceholder.typicode.com/users"

    @requests_mock.Mocker()
    def test_fetch_random_user_success(self, mock_request):
        """
        Test fetch_random_user for successful response.
        """
        mock_data = [
            {"id": 1, "name": "John Doe", "username": "johndoe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Doe", "username": "janedoe", "email": "jane@example.com"},
        ]

        mock_request.get(self.user_url, json=mock_data)

        result = External.fetch_random_user()

        self.assertIn("name", result)
        self.assertIn("email", result)
        self.assertIn("username", result)
        self.assertTrue(isinstance(result["name"], str))
        self.assertTrue(isinstance(result["email"], str))
        self.assertTrue(isinstance(result["username"], str))

    @requests_mock.Mocker()
    def test_fetch_random_user_http_error(self, mock_request):
        """
        Test fetch_random_user when an HTTP error occurs.
        """
        mock_request.get(self.user_url, status_code=500)

        with self.assertRaises(HTTPException) as context:
            External.fetch_random_user()

        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.detail, "Error fetching users from external API")

    def test_fetch_random_user_actual_request(self):
        """
        Test fetch_random_user with an actual API request.
        """
        try:
            result = External.fetch_random_user()
            self.assertIn("name", result)
            self.assertIn("email", result)
            self.assertIn("username", result)
            self.assertTrue(isinstance(result["name"], str))
            self.assertTrue(isinstance(result["email"], str))
            self.assertTrue(isinstance(result["username"], str))
        except HTTPException as e:
            self.fail(f"HTTPException raised unexpectedly: {e.detail}")
