"""
Command to wait for the database before django will start
"""

import time
from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopq2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Wait for database command
    """

    def handle(self, *args, **options):
        """Command handler"""
        self.stdout.write("Waiting for data base ...")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopq2Error, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 sec.")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available."))
