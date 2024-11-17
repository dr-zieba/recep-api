"""Tests user api"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests for unauthenticated requests"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test successful user creation"""
        payload = {
            "email": "test@example.com",
            "password": "password",
            "name": "Test user",
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload.get("email"))
        self.assertTrue(user.check_password(payload.get("password")))
        self.assertNotIn("password", response.data)

    def test_create_user_email_exists_error(self):
        """Test if user with same email can be created"""
        payload = {
            "email": "test1@example.com",
            "password": "password",
            "name": "Test user",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short_error(self):
        """Test password length"""
        payload = {
            "email": "test2@example.com",
            "password": "pass",
            "name": "Test user",
        }
        response = self.client.post(CREATE_USER_URL, **payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = (
            get_user_model().objects.filter(email=payload.get("email")).exists()
        )
        self.assertFalse(user_exist)

    def test_create_token(self):
        """Test token generation"""
        payload_create_user = {
            "email": "test3@example.com",
            "password": "password",
            "name": "Test user 3",
        }
        create_user(**payload_create_user)

        payload_user = {
            "email": payload_create_user.get("email"),
            "password": payload_create_user.get("password"),
        }
        res = self.client.post(TOKEN_URL, payload_user)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_wrong_creadentials(self):
        """Test token generation with invalid values"""
        payload_create_user = {
            "email": "test4@example.com",
            "password": "password",
            "name": "Test user 4",
        }
        create_user(**payload_create_user)

        payload_user = {
            "email": payload_create_user.get("email"),
            "password": "passworddd",
        }
        res = self.client.post(TOKEN_URL, payload_user)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_empty_password(self):
        """Test token generation with blank password"""
        payload_user = {"email": "test4@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload_user)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Auth is required for user"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test api requires auth"""

    def setUp(self):
        self.user = create_user(
            email="user@example.com", password="password", name="Test User"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test getting authed user profile"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"name": "Test User", "email": "user@example.com"}
        )

    def test_post_me_not_allowed(self):
        """Test POST is not allowed"""
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile by authed user"""
        payload = {"name": "Updated", "password": "pass123"}
        response = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "Updated")
        self.assertTrue(self.user.check_password(payload.get("password")))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
