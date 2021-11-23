import json
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, serializers, status, viewsets
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from vibbra_ecommerce_api.core.models import Bid, Deal, PhotoDeal
from rest_framework.parsers import MultiPartParser
from vibbra_ecommerce_api.core.permissions import ReadOnly
from vibbra_ecommerce_api.core.serializer import BidSerializer, DealSerializer, DeliveryPostSerializer, PhotoDealSerializer
from CorreiosPrecoPrazo.core import Correios


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        deal_id = self.kwargs.get('deal_pk')
        bids = Bid.objects.filter(deal=deal_id)
        return bids


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    http_method_names = ['get', 'post', 'put']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if request.FILES:
            photos = request.FILES
            for photo in photos:
                PhotoDeal.objects.create(deal=instance, image=photos[photo])
        return Response(serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise exceptions.PermissionDenied(
                'without permission.', 'user_cannot_edit_deal_another_user')
        if request.FILES:
            photos = request.FILES
            instance.photodeal_set.all().delete()
            for photo in photos:
                PhotoDeal.objects.create(deal=instance, image=photos[photo])
        return super(DealViewSet, self).update(request, args, kwargs)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()


@swagger_auto_schema(method="POST", request_body=DeliveryPostSerializer)
@api_view(['POST'])
def deliveries(request, deal_pk):
    serializer = DeliveryPostSerializer(data=request.data)
    if serializer.is_valid():
        deal = Deal.objects.get(pk=deal_pk)
        consulta = Correios()
        try:
            r = consulta.calculate('CalcPrecoPrazo', {
                'cd_servico': '04014',
                'cep_origem': request.user.location.zip_code,
                'cep_destino': deal.location.zip_code,
                'vl_peso': serializer.data['weight'],
                'cd_formato': serializer.data['format'],
                'vl_largura': serializer.data['width'],
                'vl_altura': serializer.data['height'],
                'vl_comprimento': serializer.data['length'],
                'valor_declarado': deal.value
            })
        except Exception as error:
            raise serializers.ValidationError({'error': error})
        return Response(r, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
