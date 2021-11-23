from django.contrib.auth import get_user_model
from django.test import TestCase

from model_mommy import mommy

from vibbra_ecommerce_api.core.models import Deal, PhotoDeal
from vibbra_ecommerce_api.location.models import Location

User = get_user_model()


class PhotoDealModelTest(TestCase):
    def setUp(self):
        user = mommy.make(User)
        location = mommy.make(Location)
        self.deal = Deal(
            user=user,
            location=location,
            type=Deal.SELL,
            value=10090.90,
            description="Macbook air pro M2",
            trade_for="None. Only sell.",
        )
        self.photo_deal = PhotoDeal(
            deal=self.deal,
            image='path/to/image'
        )

    def test_attrs(self):
        self.assertEqual(self.photo_deal.deal, self.deal)
        self.assertEqual(self.photo_deal.image, 'path/to/image')
