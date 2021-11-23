from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from vibbra_ecommerce_api.core.models import Deal
from vibbra_ecommerce_api.core.permissions import ReadOnly
from vibbra_ecommerce_api.message.models import Message
from vibbra_ecommerce_api.message.serializer import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        deal_id = self.kwargs.get('deal_pk')
        messages = Message.objects.filter(deal=deal_id)
        return messages
