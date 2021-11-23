from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy

from vibbra_ecommerce_api.location.models import Location

User = get_user_model()


class LocationModelTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.location = Location(
            user=self.user,
            lat=-77.0364,
            lng=-77.0364,
            address="Street Foo Bar",
            city="Foo",
            state="Bar",
            zip_code="55555-555",
        )

    def test_attrs(self):
        self.assertEqual(self.location.user, self.user)
        self.assertEqual(self.location.lat, -77.0364)
        self.assertEqual(self.location.lng, -77.0364)
        self.assertEqual(self.location.address, "Street Foo Bar")
        self.assertEqual(self.location.city, "Foo")
        self.assertEqual(self.location.state, "Bar")
        self.assertEqual(self.location.zip_code, "55555-555")
