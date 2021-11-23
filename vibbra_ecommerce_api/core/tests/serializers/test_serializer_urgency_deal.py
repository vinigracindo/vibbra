from django.test import TestCase
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.core.models import UrgencyDeal, Deal
from vibbra_ecommerce_api.core.serializer import UrgencyDealSerializer
from model_mommy import mommy


User = get_user_model()


class UrgencyDealerializerTest(TestCase):
    def setUp(self):
        deal = mommy.make(Deal)
        self.urgency_deal = UrgencyDeal(
            deal=deal,
            type=UrgencyDeal.URGENCY_LOW,
            limit_date='2021-12-12'
        )
        self.serializer = UrgencyDealSerializer(instance=self.urgency_deal)
        self.data = self.serializer.data

    def test_attrs_serializer(self):
        self.assertEqual(set(self.data.keys()), set(
            ['type', 'type_description', 'limit_date']))

    def test_attrs_values(self):
        self.assertEqual(self.data['type'], self.urgency_deal.type)
        self.assertEqual(self.data['type_description'],
                         self.urgency_deal.get_type_display())
        self.assertEqual(self.data['limit_date'], self.urgency_deal.limit_date)
