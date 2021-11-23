from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework.authtoken.models import Token

from vibbra_ecommerce_api.authenticate.views import SSOAuthView


User = get_user_model()


class AuthenticationSSOTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.url = reverse('auth:login-sso')
        self.user = User.objects.create_user(
            username='user', password='123456')
        self.authsso_view = SSOAuthView.as_view()

    def test_valid_authsso(self):
        token = Token.objects.create(user=self.user)
        request = self.req.post(self.url, {
            'app_token': token.key, 'login': self.user.username})
        response = self.authsso_view(request)
        self.assertTrue(response.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_authsso(self):
        request = self.req.post(self.url, {
            'app_token': 'any', 'login': self.user.username})
        response = self.authsso_view(request)
        self.assertTrue(response.data['error'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
