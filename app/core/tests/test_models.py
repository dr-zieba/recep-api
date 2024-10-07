"""
Model test cases
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Model test class"""
    def test_create_user_with_email_success(self):
        """Test succesfully created user with email"""
        email = 'test@test.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))