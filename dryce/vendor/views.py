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

#import models.py from vendor
from vendor.models import Vendor

#import serializers.py from vendor
from vendor.serializers import VendorDetailsSerializer


def sendEmail(subject, message, from_email, recipient):
    try:
        send_mail(subject, message, from_email, recipient)
        return True
    except Exception as e:
        print(e)
        return False
# Create your views here.

class CreateVendorView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classses = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #check if email exists
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        #check if username exists
        elif User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            #generate user token
            token = Token.objects.create(user=serializer.instance)
            token = token.key

            #generate otp
            otp = ''.join(str(random.randint(0,9)) for i in range(4))
            
            user = User.objects.get(username=serializer.data['username'])
            Vendor.objects.create(
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


class LogoutVendorAPIView(APIView):
    
    def get(self, request,):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        #delete the token
        data = dict(request.data)["token"]
        token = Token.objects.get(key=data)
        token.delete()
        return Response(status=status.HTTP_200_OK)

class VerifyVendorAPIView(APIView):
    def post(self, request):
        data = dict(request.data)
        user = Token.objects.get(key=data["token"]).user
        vendor = Vendor.objects.get(user=user)
        if vendor.otp == data['otp']:
            vendor.verified = True
            vendor.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
class ResetOTPAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            vendor = Vendor.objects.get(user=user)
            if vendor.verified:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                otp = ''.join(str(random.randint(0,9)) for i in range(4))
                vendor.otp = otp
                vendor.save()
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

class SearchVendorAPIView(APIView):
    def post(self, request):
        data = dict(request.data)
        user = User.objects.get(username__icontains=data['username'])
        serializer = VendorViewSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorDetailsAPIView(APIView):
    def get(self, request):
        user = request.user
        vendor = Vendor.objects.get(user=user)
        serializer = VendorDetailsSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            data = dict(request.data)
            user = request.user
            vendor = Vendor.objects.get(user=user)
            serializer = VendorDetailsSerializer(vendor, data=data)
            if serializer.is_valid():
                print(True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print(False)
                print(serializer.data)
                return Response(serializer.errors, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RatingVendorAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            vendor = Vendor.objects.get(user=user)
            serializer = VendorRatingSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)