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

class RegularUserView(serializers.ModelSerializer):
    class Meta:
        model = VendorDetails
        fields = ('id','business_certificate','resume','business_name','phone_number',' business_picture','location')

class ResetOTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=True)
    class Meta:
        model = RegularUser
        fields = ('otp',)
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('email', 'otp', 'password',)

class SearchRegularUserSerializer(serializers.ModelSerializer):
    model = RegularUser
    fields = ('id', 'user')

