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