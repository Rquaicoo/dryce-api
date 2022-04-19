from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
import random
from django.contrib.auth.models import User
#import send_mail
from django.core.mail import send_mail


def sendEmail(subject, message, from_email, recipient):
    try:
        send_mail(subject, message, from_email, recipient)
        return True
    except Exception as e:
        print(e)
        return False
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
        token = Token.objects.create(user=serializer.instance).key

        #generate otp
        otp = ''.join(str(random.randint(0,9)) for i in range(4))
        
        user = User.objects.get(username=serializer.data['username'])
        RegularUser.objects.create(
            user = user,
            otp = otp,
        )

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
        user = Token.objects.get(key=data["token"]).user
        regular_user = RegularUser.objects.get(user=user)
        if regular_user.otp == data['otp']:
            regular_user.verified = True
            regular_user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
class OTPAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            regular_user = RegularUser.objects.get(user=user)
            if regular_user.verified:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                otp = ''.join(str(random.randint(0,9)) for i in range(4))
                regular_user.otp = otp
                regular_user.save()
                send_mail('OTP', 'Your OTP is ' + otp, 'dryce.com', [user.email], fail_silently=True)
                return Response(status=status.HTTP_200_OK)

    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(email=data['email'])
        otp = ''.join(str(random.randint(0,9)) for i in range(4))
        user.otp = otp
        user.save()
        send_mail('OTP', 'Your OTP is ' + otp, 'dryce.com', [data['email']], fail_silently=True)
        return Response(status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(email=data['email'])
        if data['otp'] == user.otp:
            user.set_password(data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)

class SearchRegulerUserAPIView(APIView):
    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(username__icontains=data['username'])
        serializer = SearchRegularUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

