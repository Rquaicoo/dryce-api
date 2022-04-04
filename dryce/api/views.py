from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
import random
from django.contrib.auth import User
#import send_mail
from django.core.mail import send_mail
# Create your views here.

class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classses = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        #generate user token
        token = Token.objects.create(user=serializer.instance)

        #generate otp
        otp = ''.join(str(random.randint(0,9)) for i in range(6))
        
        user = User.objects.get(username=serializer.data['username'])
        user.otp = otp
        user.save()

        #send otp to user
        send_mail('OTP', 'Your OTP is ' + otp, 'dryce.com', [serializer.data['email']], fail_silently=True)


        token_data = {"token": token}
        return Response(
            {**serializer.data, **token_data},
            status = status.HTTP_201_CREATED,
            headers=headers
        )


class LogoutUserAPIView(APIView):
    
    def get(self, request,):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        #delete the token
        data = dict(request.data)["token"]
        token = Token.objects.get(key=data)
        token.delete()
        return Response(status=status.HTTP_200_OK)

class VerifyUserAPIView(APIView):
    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(username=data['token'])
        if user.otp == data['otp']:
            user.verified = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
