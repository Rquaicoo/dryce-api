from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)




