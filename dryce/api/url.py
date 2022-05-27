from cgitb import reset
from django import views
from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('auth/register/', CreateUserView.as_view(), name="register"),
    path('auth/validate_email/', ValidEmailAPIView.as_view(), name="validate_email"),
    path('auth/validate_username/', ValidUsernameAPIView.as_view(), name="validate_username"),

    path('auth/login/', obtain_auth_token, name="login"),
    path('auth/logout/', LogoutUserAPIView.as_view(), name="logout"),
    path('auth/verify_user/', VerifyUserAPIView.as_view(), name="verify_user"),
    path('auth/vendor/register/', CreateUserView.as_view(), name="vendor_register"),
    path('auth/resend_otp/', OTPAPIView.as_view(), name="resend_otp"),
    path('auth/reset_password/', ResetPasswordAPIView.as_view(), name="reset_password"),
    path('cart/', CartAPIView.as_view(), name="cart"),
    path('rating/', RatingAPIView.as_view(), name="rating"),
    path('contact/', ContactAPIView.as_view(), name="contact"),
]