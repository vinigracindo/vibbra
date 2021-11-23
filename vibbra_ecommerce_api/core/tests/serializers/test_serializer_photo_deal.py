from django.test import TestCase
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.core.models import PhotoDeal, Deal
from vibbra_ecommerce_api.core.serializer import PhotoDealSerializer
from model_mommy import mommy


User = get_user_model()


class PhotoDealSerializerTest(TestCase):
    def setUp(self):
        deal = mommy.make(Deal)
        self.photo_deal = PhotoDeal(
            deal=deal,
            image='/path/to/image'
        )
        self.serializer = PhotoDealSerializer(instance=self.photo_deal)
        self.data = self.serializer.data

    def test_attrs_serializer(self):
        self.assertEqual(set(self.data.keys()), set(['image']))

    def test_attrs_values(self):
        self.assertEqual(self.data['image'], self.photo_deal.image.url)
