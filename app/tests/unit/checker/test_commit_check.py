"""
These tests cover the functionality of the PylintChecker class,
ensuring that the pylint score checking logic works correctly under various conditions.
"""

import unittest
from unittest.mock import patch, MagicMock
from app.scripts import PylintChecker


class TestPylintChecker(unittest.TestCase):
    """
    Unit tests for the PylintChecker class.

    """

    def setUp(self):
        """
        Setup for the tests.
        """
        self.checker = PylintChecker(threshold=9.0)

    @patch("subprocess.run")
    def test_run_pylint_successful(self, mock_run):
        """
        Test the run_pylint method for a successful pylint execution.
        """
        mock_run.return_value = MagicMock(stdout="Your code has been rated at 9.5/10", returncode=0)

        output, returncode = self.checker.run_pylint()
        self.assertEqual(output, "Your code has been rated at 9.5/10")
        self.assertEqual(returncode, 0)

    @patch("subprocess.run")
    def test_check_score_sufficient(self, mock_run):
        """
        Test the check_score method when the pylint score is sufficient.
        """
        mock_run.return_value = MagicMock(stdout="Your code has been rated at 9.5/10", returncode=0)

        with patch("sys.exit") as mock_exit:
            output, _ = self.checker.run_pylint()
            self.checker.check_score(output)
            mock_exit.assert_called_with(0)

    @patch("subprocess.run")
    def test_check_score_insufficient(self, mock_run):
        """
        Test the check_score method when the pylint score is insufficient.
        """
        mock_run.return_value = MagicMock(stdout="Your code has been rated at 8.0/10", returncode=0)

        with patch("sys.exit") as mock_exit:
            output, _ = self.checker.run_pylint()
            self.checker.check_score(output)
            mock_exit.assert_called_with(1)

    @patch("subprocess.run")
    def test_check_score_not_found(self, mock_run):
        """
        Test the check_score method when the pylint score is not found in the output.
        """
        mock_run.return_value = MagicMock(stdout="Some other output", returncode=0)

        with patch("sys.exit") as mock_exit:
            output, _ = self.checker.run_pylint()
            self.checker.check_score(output)
            mock_exit.assert_called_with(1)
