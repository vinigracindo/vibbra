from django.contrib.auth import get_user_model
from django.db import models
from vibbra_ecommerce_api.core.models import Deal


User = get_user_model()


class Message(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    message = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
