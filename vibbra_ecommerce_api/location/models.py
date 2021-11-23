from django.db import models


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.TextField()
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=15)
