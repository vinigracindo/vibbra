from django.test import TestCase
from vibbra_ecommerce_api.authenticate.serializer import SSOAuthSerializer


class SSOAuthSerializerTest(TestCase):
    def setUp(self):
        data = {'app_token': 'token', 'login': 'username'}
        self.serializer = SSOAuthSerializer(data=data)
        self.serializer.is_valid()

    def test_is_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_attrs_serializers(self):
        self.assertEqual(set(self.serializer.data.keys()),
                         set(['app_token', 'login']))
