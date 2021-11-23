from django.test import TestCase
from vibbra_ecommerce_api.location.models import Location
from vibbra_ecommerce_api.location.serializer import LocationSerializer


class LocationSerializerTest(TestCase):
    def setUp(self):
        self.location = Location(
            lat=-77.0364,
            lng=-77.0364,
            address="Street Foo Bar",
            city="Foo",
            state="Bar",
            zip_code="55555-555",
        )
        self.serializer = LocationSerializer(instance=self.location)
        self.data = self.serializer.data

    def test_attrs_serializers(self):
        self.assertEqual(set(self.data.keys()), set(
            ['lat', 'lng', 'address', 'city', 'state', 'zip_code']))

    def test_attrs_values(self):
        self.assertEqual(self.data['lat'], self.location.lat)
        self.assertEqual(self.data['lng'], self.location.lng)
        self.assertEqual(self.data['address'], self.location.address)
        self.assertEqual(self.data['city'], self.location.city)
        self.assertEqual(self.data['state'], self.location.state)
        self.assertEqual(self.data['zip_code'], self.location.zip_code)
