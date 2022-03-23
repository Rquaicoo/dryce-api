from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('auth/register/', CreateUserView.as_view(), name="register"),
    path('auth/login/', obtain_auth_token, name="login"),
    path('auth/logout/', LogoutUserAPIView.as_view(), name="logout")
]