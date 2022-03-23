from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return str(self.user.username)
