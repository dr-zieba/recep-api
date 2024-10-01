"""
Command to wait for the database before django will start
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Wait for database command
    """

    def handle(self, *args, **options):
        pass
