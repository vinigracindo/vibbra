from django.db import models
from django.contrib.auth.models import AbstractUser

from vibbra_ecommerce_api.location.models import Location


class User(AbstractUser):
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'authenticate'
