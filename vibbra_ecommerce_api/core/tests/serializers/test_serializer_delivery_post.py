from django.test import TestCase
from django.contrib.auth import get_user_model
from vibbra_ecommerce_api.core.serializer import DeliveryPostSerializer
from model_mommy import mommy


User = get_user_model()


class DeliveryPostSerializerTest(TestCase):
    def setUp(self):
        data = {
            'weight': 2.28,
            'format': 'rolo',
            'width': 1.01,
            'height': 2.64,
            'length': 3.14,
        }
        self.serializer = DeliveryPostSerializer(data=data)
        self.serializer.is_valid()
        self.data = self.serializer.data

    def test_attrs_serializer(self):
        self.assertEqual(set(self.data.keys()), set(
            ['weight', 'format', 'width', 'height', 'length']))
