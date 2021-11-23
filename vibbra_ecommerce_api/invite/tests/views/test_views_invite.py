from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy
from vibbra_ecommerce_api.invite.models import Invite
from vibbra_ecommerce_api.invite.views import InviteViewSet


User = get_user_model()


class InviteListViewSetTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.user = mommy.make(User)
        self.invite = Invite.objects.create(
            user=self.user,
            name='name',
            email='foo@bar.com'
        )
        self.url = reverse('invite:invites-list',
                           kwargs={'user_pk': self.user.pk})

    def test_without_auth(self):
        invite_view = InviteViewSet.as_view({'get': 'list'})
        request = self.req.get(self.url)
        response = invite_view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        invite_view = InviteViewSet.as_view({'get': 'list'})
        request = self.req.get(self.url)
        force_authenticate(request, user=self.user)
        response = invite_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        invite_view = InviteViewSet.as_view({'post': 'create'})
        data = {
            'name': 'name',
            'email': 'example@mail.com'
        }
        request = self.req.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        response = invite_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invite = Invite.objects.last()
        self.assertEqual(invite.user, self.user)


class InviteDetailViewSetTestCase(APITestCase):
    def setUp(self):
        self.req = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user', password='123456')
        self.invite = Invite.objects.create(
            user=self.user,
            name='name',
            email='foo@bar.com'
        )
        self.url = reverse('invite:invites-detail',
                           kwargs={'user_pk': self.user.pk, 'pk': self.invite.pk})

    def test_delete(self):
        invite_view = InviteViewSet.as_view({'delete': 'destroy'})
        request = self.req.delete(self.url, format='json')
        force_authenticate(request, user=self.user)
        response = invite_view(request, pk=self.user.pk)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
