"""
Model test cases
"""

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Model test class"""

    def test_create_user_with_email_success(self):
        """Test succesfully created user with email"""
        email = "test@test.com"
        password = "password"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Creating user with normalized email address"""
        emails = [
            "user1@example.com",
            "user2@EXAMPLE.COM",
            "user3@example.COM",
            "user4@EXAMPLE.com",
        ]
        password = "password"
        for id, email in enumerate(emails, start=1):
            user = get_user_model().objects.create_user(email, password)
            self.assertEqual(user.email, f"user{id}@example.com")

    def test_new_user_without_email_raises_error(self):
        """Creating user without email raises exception"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="password")

    def test_crate_super_user(self):
        """Create superuser"""
        user = get_user_model().objects.create_superuser(
            email="test2@test.com", password="password"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test create recipe api"""
        user = get_user_model().objects.create_user("test@example.com", "pass123")
        recipe = models.Recipe.objects.create(
            user=user,
            title="Test title",
            time_minutes=5,
            price=Decimal("5.5"),
            description="Test description",
        )
        self.assertEqual(str(recipe), recipe.title)
