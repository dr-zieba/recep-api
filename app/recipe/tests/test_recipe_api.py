"""
Test for recipe apis
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **kwargs):
    """Creates example recipe"""
    defaults = {
        "title": "Test recipe",
        "description": "Test description",
        "time_minutes": 5,
        "price": Decimal("5.7"),
        "link": "Test link",
    }
    defaults.update(kwargs)
    print(defaults)
    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeApiTests(TestCase):
    """Test for none-authorized api calls"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test if auth is required to make a call"""
        response = self.client.get(RECIPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Tests for authorized users"""

    def setUp(self):

        default_user = {
            "email": "user@example.com",
            "password": "pass123",
            "name": "Test user",
        }

        self.client = APIClient()
        self.user = get_user_model().objects.create(**default_user)
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe(self):
        """Test listing recipes"""
        create_recipe(self.user)
        create_recipe(self.user)

        response = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_retrieve_for_user_specific(self):
        """Test listing recipes for user"""
        other_user = get_user_model().objects.create_user(
            "other@example.com", "pass4321"
        )
        create_recipe(other_user)
        create_recipe(self.user)

        response = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
