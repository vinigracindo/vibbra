from django.test import TestCase
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.core.models import Bid, Deal
from vibbra_ecommerce_api.core.serializer import BidSerializer
from model_mommy import mommy


User = get_user_model()


class BidSerializerTest(TestCase):
    def setUp(self):
        user = mommy.make(User)
        deal = mommy.make(Deal)
        self.bid = Bid(
            user=user,
            deal=deal,
            accepted=True,
            value=100,
            description='a description...'
        )
        self.serializer = BidSerializer(instance=self.bid)
        self.data = self.serializer.data

    def test_attrs_serializer(self):
        self.assertEqual(set(self.data.keys()), set(
            ['id', 'deal', 'accepted', 'value', 'description', 'user']))

    def test_attrs_values(self):
        self.assertEqual(self.data['deal'], self.bid.deal.pk)
        self.assertEqual(self.data['accepted'], self.bid.accepted)
        self.assertEqual(float(self.data['value']), self.bid.value)
        self.assertEqual(self.data['description'], self.bid.description)
        self.assertEqual(self.data['user'], self.bid.user.pk)
