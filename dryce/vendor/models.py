from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, blank=True, null=True)
    verified = models.BooleanField(default=False)
    certified = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

        
class VendorDetails(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, blank=False)

    business_name=models.CharField(max_length=100, blank=False, null=False) 
    phone_number=models.CharField(max_length=10, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=100, blank=False, null=False)
    business_description = models.CharField(max_length=100, blank=False, null=False)
    business_certificate=models.FileField(blank=False)
     
    business_picture=models.ImageField(blank=True)
    business_logo=models.ImageField(blank=True)

    opening_hours=models.CharField(max_length=100, blank=True, null=True)
    closing_hours=models.CharField(max_length=100, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.vendor)  
