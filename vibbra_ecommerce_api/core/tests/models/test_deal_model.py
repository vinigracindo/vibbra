import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy

from vibbra_ecommerce_api.core.models import Deal
from vibbra_ecommerce_api.location.models import Location

User = get_user_model()


class LocationModelTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.location = mommy.make(Location)
        self.deal = Deal(
            user=self.user,
            location=self.location,
            type=Deal.SELL,
            value=10090.90,
            description="Macbook air pro M2",
            trade_for="None. Only sell.",
        )

    def test_attrs(self):
        self.assertEqual(self.deal.user, self.user)
        self.assertEqual(self.deal.location, self.location)
        self.assertEqual(self.deal.type, 1)
        self.assertEqual(self.deal.value, 10090.90)
        self.assertEqual(self.deal.description, "Macbook air pro M2")
        self.assertEqual(self.deal.trade_for, "None. Only sell.")
