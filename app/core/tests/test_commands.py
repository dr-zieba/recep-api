"""
Test commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopq2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check") 
class CommandTest(SimpleTestCase):
    """Test class for commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test when db is ready"""
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_not_ready(self, patched_sleep, patched_check):
        """Test when db is not ready"""

        # Simulates checks with returned values like Psycopq2Error,
        # OperationalError and True = db finally got ready
        patched_check.side_effect = [Psycopq2Error] * 2 + [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])

