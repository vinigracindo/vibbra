from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from vibbra_ecommerce_api.location.models import Location
from vibbra_ecommerce_api.location.serializer import LocationSerializer
from vibbra_ecommerce_api.core.models import Bid, Deal, PhotoDeal, UrgencyDeal

User = get_user_model()


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deal']

    def create(self, validated_data):
        request = self.context.get('request')
        deal_pk = request.parser_context.get('kwargs').get('deal_pk')
        validated_data['deal'] = Deal.objects.get(pk=deal_pk)
        bid = Bid.objects.create(**validated_data)
        return bid


class PhotoDealSerializer(serializers.ModelSerializer):
    image = serializers.FileField(read_only=False, required=False)

    class Meta:
        model = PhotoDeal
        fields = ['image']

    def create(self, validated_data):
        deal = Deal.objects.latest('created_at')
        image = validated_data.pop('image')
        photos = []
        for img in image:
            photos.append(PhotoDeal.objects.create(deal=deal, image=img))
        return photos


class UrgencyDealSerializer(serializers.ModelSerializer):
    type_description = serializers.SerializerMethodField()

    class Meta:
        model = UrgencyDeal
        exclude = ['id', 'deal']

    def get_type_description(self, obj):
        return obj.get_type_display()


class DealSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    urgency = UrgencyDealSerializer(
        many=False, read_only=False, source='urgencydeal')
    type_description = serializers.SerializerMethodField()
    photos = PhotoDealSerializer(many=True, source='photodeal_set')
    location = LocationSerializer(many=False, read_only=False)

    class Meta:
        model = Deal
        fields = ['id', 'type', 'type_description', 'value', 'description',
                  'trade_for', 'location', 'urgency', 'photos', 'user']

    def get_type_description(self, obj):
        return obj.get_type_display()

    def validate(self, data):
        return data

    @transaction.atomic
    def create(self, validated_data):
        urgency_data = validated_data.pop('urgencydeal')
        location_data = validated_data.pop('location')
        photos_data = validated_data.pop('photodeal_set')
        location = Location.objects.create(**location_data)
        deal = Deal.objects.create(**validated_data, location=location)
        UrgencyDeal.objects.create(**urgency_data, deal=deal)
        return deal

    @transaction.atomic
    def update(self, instance, validated_data):
        urgency_data = validated_data.pop('urgencydeal')
        location_data = validated_data.pop('location')
        photos_data = validated_data.pop('photodeal_set')

        instance.user = validated_data.get('user')
        instance.type = validated_data.get('type')
        instance.value = validated_data.get('value')
        instance.login = validated_data.get('login')
        instance.description = validated_data.get('description')
        instance.trade_for = validated_data.get('trade_for')
        instance.save()

        data = {
            'lat': location_data.get('lat'),
            'lng': location_data.get('lng'),
            'address': location_data.get('address'),
            'city': location_data.get('city'),
            'state': location_data.get('state'),
            'zip_code': location_data.get('zip_code'),
        }

        Location.objects.filter(
            pk=instance.location.pk).update(**data)

        data = {
            'type': urgency_data.get('type'),
            'limit_date': urgency_data.get('limit_date')
        }

        UrgencyDeal.objects.filter(pk=instance.urgencydeal.pk).update(**data)

        instance.refresh_from_db()

        return instance


class DeliveryPostSerializer(serializers.Serializer):
    weight = serializers.FloatField()
    format = serializers.ChoiceField(choices=['caixa', 'rolo', 'envelope'])
    width = serializers.FloatField()
    height = serializers.FloatField()
    length = serializers.FloatField()
