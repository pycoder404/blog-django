from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """
    avatar = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, default='InSite')
    roles = models.CharField(max_length=255, default='dev')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
