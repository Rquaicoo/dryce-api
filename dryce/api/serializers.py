from dataclasses import field
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, 
    required=True,
    style={'input_type':'password'})

    class Meta:
        model = get_user_model()
        fields = ('username','email','password','is_active', 'date_joined', 'last_login')
        write_only_fields = ('password')
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class RegularUserView(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = ('id','user',)

class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = ('id','otp')

class ResetOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = ('otp',)
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'otp', 'password',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','is_active', 'last_login')

class SearchRegularUserSerializer(serializers.ModelSerializer):
    model = RegularUser
    fields = ('id', 'user')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'identifier', 'tshirts', 
        'jeans', 'siglets', 'jackets', 'trousers', 'suits', 
        'blazers', 'skirts', 'blouses', 'ties', 'cost')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')
