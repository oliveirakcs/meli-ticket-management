"""
External API Interaction Module
"""

import logging
import random
import requests
from fastapi import HTTPException

JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class External:
    """
    A class for handling external API interactions.
    """

    @staticmethod
    def fetch_random_comment() -> dict:
        """
        Fetch a random comment from JSONPlaceholder.

        Returns:
            dict: A dictionary containing the comment body and user email.

        Raises:
            HTTPException: If there's an issue fetching comments from the external API.
        """
        try:
            response = requests.get(f"{JSONPLACEHOLDER_URL}/comments", timeout=10)
            response.raise_for_status()
            comments = response.json()

            if not comments:
                raise HTTPException(status_code=404, detail="No comments found.")

            random_comment = random.choice(comments)
            comment_text = random_comment["body"].replace("\n", " ")
            comment_user = random_comment["email"]

            return {"comment_text": comment_text, "comment_user": comment_user}

        except requests.HTTPError as e:
            logger.error("Error fetching comments from external API: %s", e)
            raise HTTPException(status_code=response.status_code, detail="Error fetching comments from external API") from e
        except Exception as e:
            logger.error("Error fetching comments: %s", e)
            raise HTTPException(status_code=500, detail=str(e)) from e

    @staticmethod
    def fetch_random_user() -> dict:
        """
        Fetch a random user from JSONPlaceholder.

        Returns:
            dict: A dictionary containing the user name, email, and username.

        Raises:
            HTTPException: If there's an issue fetching users from the external API.
        """
        try:
            response = requests.get(f"{JSONPLACEHOLDER_URL}/users", timeout=10)
            response.raise_for_status()
            users = response.json()

            if not users:
                raise HTTPException(status_code=404, detail="No users found.")

            random_user = random.choice(users)
            return {"name": random_user["name"], "email": random_user["email"], "username": random_user["username"]}

        except requests.HTTPError as e:
            logger.error("Error fetching users from external API: %s", e)
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching users from external API") from e
        except Exception as e:
            logger.error("Error fetching users: %s", e)
            raise HTTPException(status_code=500, detail=str(e)) from e
