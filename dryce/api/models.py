from django.db import models
from django.contrib.auth.models import User
from vendor.models import Vendor
# Create your models here.

class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

class Cart(models.Model):
    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, blank=True, null=True)
    tshirts = models.IntegerField(blank=True, null=True)
    jeans = models.IntegerField(blank=True, null=True)
    siglets = models.IntegerField(blank=True, null=True)
    jackets = models.IntegerField(blank=True, null=True)
    trousers = models.IntegerField(blank=True, null=True)
    suits = models.IntegerField(blank=True, null=True)
    blazers = models.IntegerField(blank=True, null=True)
    skirts = models.IntegerField(blank=True, null=True)
    blouses = models.IntegerField(blank=True, null=True)
    ties = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

class VendorChat(models.Model):
    user = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    reciever = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reciever')
    message = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


