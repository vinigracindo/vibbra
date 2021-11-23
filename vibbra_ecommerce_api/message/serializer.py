from rest_framework import serializers
from vibbra_ecommerce_api.core.models import Deal
from vibbra_ecommerce_api.message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['deal']

    def create(self, validated_data):
        request = self.context.get('request')
        deal_pk = request.parser_context.get('kwargs').get('deal_pk')
        validated_data['deal'] = Deal.objects.get(pk=deal_pk)
        message = Message.objects.create(**validated_data)
        return message
