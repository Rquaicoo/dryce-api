from datetime import datetime
from pyexpat import model
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from vendor.models import Vendor
# Create your models here.

class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, blank=True, null=True)
    verified = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Cart(models.Model):
    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    cost = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    service = models.CharField(max_length=100, blank=True, null=True)

    identifier = models.CharField(max_length=10, blank=True, null=True)
    
    shirts = models.IntegerField(blank=True, null=True)
    jeans = models.IntegerField(blank=True, null=True)

    cardigans = models.IntegerField(blank=True, null=True)
    trousers = models.IntegerField(blank=True, null=True)

    dress = models.IntegerField(blank=True, null=True)
    blouses = models.IntegerField(blank=True, null=True)
    

    def __str__(self):
        return str(self.user)

class Order(models.Model):
    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=15, blank=True, null=True)
    delivery = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)

class VendorChat(models.Model):
    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    reciever = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reciever')
    message = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.CharField(max_length=100, blank=False, null=False)

