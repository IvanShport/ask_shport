from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import os
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='image/%Y/%m/%d', default='/default/user.png', blank=True, null=True)

    def __str__(self):

        return self.user.username
