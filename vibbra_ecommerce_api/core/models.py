from django.db import models
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.location.models import Location


User = get_user_model()


class Deal(models.Model):
    SELL = 1
    TRADE = 2
    WISH = 3
    TYPE_CHOICES = (
        (SELL, 'Venda'),
        (TRADE, 'Troca'),
        (WISH, 'Desejo'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=128)
    trade_for = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UrgencyDeal(models.Model):
    URGENCY_LOW = 1
    URGENCY_MEDIUM = 2
    URGENCY_HIGH = 3
    URGENCY_CHOICES = (
        (URGENCY_LOW, 'Baixa'),
        (URGENCY_MEDIUM, 'Média'),
        (URGENCY_HIGH, 'Alta'),
    )

    deal = models.OneToOneField(Deal, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=URGENCY_CHOICES)
    limit_date = models.DateField()


class PhotoDeal(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='deals/images')


class Bid(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
