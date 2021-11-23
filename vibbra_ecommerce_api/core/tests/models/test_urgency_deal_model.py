from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy

from vibbra_ecommerce_api.core.models import Deal, UrgencyDeal
from vibbra_ecommerce_api.location.models import Location

User = get_user_model()


class UrgencyDealModelTest(TestCase):
    def setUp(self):
        user = mommy.make(User)
        self.deal = Deal(
            user=user,
            location=mommy.make(Location),
            type=Deal.SELL,
            value=10090.90,
            description="Macbook air pro M2",
            trade_for="None. Only sell.",
        )
        self.urgency_deal = UrgencyDeal(
            deal=self.deal,
            type=UrgencyDeal.URGENCY_HIGH,
            limit_date='2021-12-12'
        )

    def test_attrs(self):
        self.assertEqual(self.urgency_deal.deal, self.deal)
        self.assertEqual(self.urgency_deal.type, 3)
        self.assertEqual(self.urgency_deal.limit_date, '2021-12-12')
