"""
View for recipe api
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewset(viewsets.ModelViewSet):
    """View for handling recipe api"""

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """List recipes for authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-id")
