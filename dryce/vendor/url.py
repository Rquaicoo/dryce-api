from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/register/', CreateVendorView.as_view(), name="register"),
    path('auth/login/', obtain_auth_token, name="login"),
    path('auth/logout/', LogoutVendorAPIView.as_view(), name="logout"),
    path('auth/verify_user/', VerifyVendorAPIView.as_view(), name="verify_user"),
    path('auth/reset_password/', ResetPasswordAPIView.as_view(), name="reset_password"),
    path('auth/reset_otp/', ResetOTPAPIView.as_view(), name="reset_otp"),


    
]