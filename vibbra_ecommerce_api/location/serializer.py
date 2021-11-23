from rest_framework import fields, serializers

from vibbra_ecommerce_api.location.models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ['id']
