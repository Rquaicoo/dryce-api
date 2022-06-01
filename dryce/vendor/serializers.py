from dataclasses import field
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import base64



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

class VendorViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id','user',)

class VendorDetailsSerializer(serializers.ModelSerializer):
    name = serializers.JSONField()
    phone = serializers.JSONField()
    address = serializers.JSONField()
    email = serializers.JSONField()
    city = serializers.JSONField()
    region = serializers.JSONField()
    description = serializers.JSONField()
    longitude = serializers.JSONField()
    latitude = serializers.JSONField()
    description = serializers.JSONField()
    picture = serializers.ImageField()

    class Meta:
        model = VendorDetails
        fields = ('id', 'name', 'phone', 'address', 'email', 'city', 'region', 'description','certificate', 'logo', 'picture', 'latitude', 'longitude')

class VerifyVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id','otp')

class VendorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id','rating','rating_count')

class ResetOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('otp')
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'otp', 'password',)



