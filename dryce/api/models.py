from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return str(self.user.username)

class VendorDetails(models.Model):
    business_certificate=models.FileField(null=True, blank=True)
    resume=models.FileField(null=True,blank=True)
    business_name=models.CharField(max_length=100) 
    Phone_number=models.CharField(max_length=100)  
    business_picture=models.ImageField(null=True, blank=True)
    Location=models.CharField(max_length=100)

    def __str__(self):
        return str(self.Name)  
