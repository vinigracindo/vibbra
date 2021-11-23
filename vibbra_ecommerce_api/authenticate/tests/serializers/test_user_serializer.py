from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy
from vibbra_ecommerce_api.authenticate.serializer import UserSerializer
from vibbra_ecommerce_api.location.models import Location
from vibbra_ecommerce_api.location.serializer import LocationSerializer


User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.serializer = UserSerializer(instance=self.user)
        self.serializer.location = LocationSerializer(
            instance=mommy.make(Location, user=self.user))
        self.data = self.serializer.data

    def test_attrs_serializers(self):
        self.assertEqual(set(self.data.keys()), set(
            ['name', 'email', 'login', 'password', 'location']))

    def test_attrs_values(self):
        self.assertEqual(self.data['name'], self.user.first_name)
        self.assertEqual(self.data['email'], self.user.email)
        self.assertEqual(self.data['login'], self.user.username)
        self.assertEqual(self.data['password'], self.user.password)
        self.assertTrue(self.data['location'])
