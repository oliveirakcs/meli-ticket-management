"""Unit tests for the Hash class using bcrypt encryption."""

import unittest
from app.core import Hash


class TestHash(unittest.TestCase):
    """Unit tests for the Hash class, which provides methods for hashing and verifying passwords."""

    def setUp(self):
        """Set up any necessary test variables."""
        self.password = "password123"
        self.wrong_password = "wrongpassword"
        self.hashed_password = Hash.bcrypt(self.password)

    def test_bcrypt(self):
        """Test the bcrypt method to ensure it hashes passwords correctly."""
        hashed = Hash.bcrypt(self.password)
        self.assertNotEqual(hashed, self.password)
        self.assertTrue(Hash.verify(self.password, hashed))

    def test_verify_correct_password(self):
        """Test the verify method to confirm it returns True for correct password verification."""
        result = Hash.verify(self.password, self.hashed_password)
        self.assertTrue(result)

    def test_verify_wrong_password(self):
        """Test the verify method to confirm it returns False for incorrect password verification."""
        result = Hash.verify(self.wrong_password, self.hashed_password)
        self.assertFalse(result)

    def test_bcrypt_consistency(self):
        """Test that bcrypt does not produce the same hash for the same password twice."""
        hash1 = Hash.bcrypt(self.password)
        hash2 = Hash.bcrypt(self.password)
        self.assertNotEqual(hash1, hash2)
        self.assertTrue(Hash.verify(self.password, hash1))
        self.assertTrue(Hash.verify(self.password, hash2))

    def test_verify_empty_password(self):
        """Test the verify method with an empty password to ensure it returns False."""
        result = Hash.verify("", self.hashed_password)
        self.assertFalse(result)
