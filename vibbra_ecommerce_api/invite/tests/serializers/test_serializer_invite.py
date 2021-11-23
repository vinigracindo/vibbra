from django.test import TestCase
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.invite.models import Invite
from vibbra_ecommerce_api.invite.serializer import InviteSerializer
from model_mommy import mommy


User = get_user_model()


class InviteSerializerTest(TestCase):
    def setUp(self):
        user = mommy.make(User)
        self.invite = Invite(
            user=user,
            name="Lorem Ipsum",
            email="lorem@ipsum.com"
        )
        self.serializer = InviteSerializer(instance=self.invite)
        self.data = self.serializer.data

    def test_attrs_serializer(self):
        self.assertEqual(set(self.data.keys()), set(['id', 'name', 'email']))

    def test_attrs_values(self):
        self.assertEqual(self.data['name'], self.invite.name)
        self.assertEqual(self.data['email'], self.invite.email)
