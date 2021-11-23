from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.urls import reverse
from rest_framework import status

from vibbra_ecommerce_api.authenticate.views import UserViewSet
from vibbra_ecommerce_api.location.models import Location


User = get_user_model()


class UserListViewSetTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.url = reverse('auth:users-list')
        self.user = User.objects.create_user(
            username='user', password='123456')

    def test_without_auth(self):
        users_view = UserViewSet.as_view({'get': 'list'})
        request = self.req.get(self.url)
        response = users_view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        users_view = UserViewSet.as_view({'get': 'list'})
        request = self.req.get(self.url)
        force_authenticate(request, user=self.user)
        response = users_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_keys = ['name', 'email', 'login', 'password', 'location']
        for key in expected_keys:
            with self.subTest("test key {}".format(key)):
                self.assertTrue(key in response.data[0])

    def test_post(self):
        users_view = UserViewSet.as_view({'post': 'create'})
        data = {
            'login': 'another_user',
            'password': '123456',
            'name': 'name',
            'email': 'foo@bar.com',
            'location': {
                'lat': 1,
                'lng': 2,
                'address': 'address',
                'city': 'city',
                'state': 'state',
                'zip_code': '11111111'
            }
        }
        request = self.req.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = users_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Location.objects.all().exists())


class UserDetailViewSetTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user', password='123456')
        self.url = reverse('auth:users-detail', kwargs={'pk': self.user.pk})

    def test_put(self):
        users_view = UserViewSet.as_view({'put': 'update'})
        data = {
            'login': 'user2',
            'password': '123456',
            'name': 'name',
            'email': 'foo@bar.com',
            'location': {
                'lat': 1,
                'lng': 2,
                'address': 'address',
                'city': 'city',
                'state': 'state',
                'zip_code': '11111111'
            }
        }
        request = self.req.put(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = users_view(request, pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual('user2', self.user.username)

    def test_delete(self):
        users_view = UserViewSet.as_view({'delete': 'destroy'})
        request = self.req.delete(self.url, format='json')
        force_authenticate(request, user=self.user)
        response = users_view(request, pk=self.user.pk)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
