from django.test import TestCase
from django.contrib.auth import get_user_model
from model_mommy import mommy

from vibbra_ecommerce_api.invite.models import Invite


User = get_user_model()


class InviteModelTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.location = Invite(
            name="name",
            email="email@email.com",
        )

    def test_attrs(self):
        self.assertEqual(self.location.name, "name")
        self.assertEqual(self.location.email, "email@email.com")
