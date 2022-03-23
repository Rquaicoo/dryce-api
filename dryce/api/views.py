from asyncio import start_unix_server
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
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

    
