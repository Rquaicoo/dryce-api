from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    certified = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

        
class VendorDetails(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, blank=False)

    business_description = models.CharField(max_length=100, blank=False, null=False)
    business_certificate=models.FileField(blank=False)
    resume=models.FileField(null=False,blank=False)
    business_name=models.CharField(max_length=100, blank=False, null=False) 
    phone_number=models.CharField(max_length=10, blank=False, null=False)  
    business_picture=models.ImageField(blank=True)

    location=models.CharField(max_length=100, null=False,blank=False)
    opening_hours=models.CharField(max_length=100, blank=True, null=True)
    closing_hours=models.CharField(max_length=100, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.vendor)  
