from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.urls import reverse
from rest_framework import status
from vibbra_ecommerce_api.core.models import Deal, Bid
from model_mommy import mommy
from vibbra_ecommerce_api.core.views import BidViewSet
from vibbra_ecommerce_api.location.models import Location


User = get_user_model()


class BidViewSetTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user', password='123456')
        self.deal = Deal.objects.create(
            user=self.user,
            location=mommy.make(Location),
            type=Deal.SELL,
            value=10090.90,
            description="Macbook air pro M2",
            trade_for="None. Only sell.",
        )
        self.url = reverse('core:bids-list', kwargs={'deal_pk': self.deal.pk})

    def test_get(self):
        invite_view = BidViewSet.as_view({'get': 'list'})
        request = self.req.get(self.url)
        response = invite_view(request, kwargs={'deal_pk': self.deal.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
