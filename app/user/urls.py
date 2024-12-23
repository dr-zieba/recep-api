"""User api urls"""

from django.urls import path
from user.views import CreateUserView, CreateTokenView, ManageUserView

# Mapping for revers urls like: reverse('user:create')
app_name = "user"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="me"),
]
