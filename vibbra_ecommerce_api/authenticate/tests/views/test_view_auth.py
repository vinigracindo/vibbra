from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse

from vibbra_ecommerce_api.authenticate.views import TokenObtainPairView


User = get_user_model()


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.url = reverse('auth:login')
        self.user = User.objects.create_user(
            username='user', password='123456')
        self.auth_view = TokenObtainPairView.as_view()

    def test_valid_auth(self):
        request = self.req.post(self.url, {
            'login': 'user', 'password': '123456'})
        response = self.auth_view(request)
        self.assertTrue(response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_auth(self):
        request = self.req.post(self.url, {
            'login': 'error', 'password': 'error'})
        response = self.auth_view(request)
        self.assertTrue(response.data['error'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
