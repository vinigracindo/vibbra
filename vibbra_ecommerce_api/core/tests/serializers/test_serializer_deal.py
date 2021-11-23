from django.test import TestCase
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.core.models import Deal
from vibbra_ecommerce_api.location.models import Location
from vibbra_ecommerce_api.core.serializer import DealSerializer
from model_mommy import mommy


User = get_user_model()


class DealSerializerTest(TestCase):
    def setUp(self):
        user = mommy.make(User)
        self.deal = Deal(
            user=user,
            location=mommy.make(Location),
            type=Deal.TRADE,
            value=100,
            description="Lorem Ipsum",
            trade_for="Computer"
        )
        self.serializer = DealSerializer(instance=self.deal)
        self.data = self.serializer.data

    def test_attrs_serializer(self):
        self.assertEqual(set(self.data.keys()), set(
            ['id', 'type', 'type_description', 'value', 'description',
             'trade_for', 'location', 'urgency', 'photos']))
