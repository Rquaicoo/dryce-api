from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    certified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

        
class VendorDetails(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, blank=False)
    business_certificate=models.FileField(blank=False)
    resume=models.FileField(null=False,blank=False)
    business_name=models.CharField(max_length=100, blank=False, null=False) 
    phone_number=models.CharField(max_length=10, blank=False, null=False)  
    business_picture=models.ImageField(blank=False)
    location=models.CharField(max_length=100, null=False,blank=False)

    def __str__(self):
        return str(self.vendor)  
