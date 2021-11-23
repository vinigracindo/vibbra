from rest_framework import fields, serializers

from vibbra_ecommerce_api.invite.models import Invite


class InviteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Invite
        exclude = ['created_at', 'updated_at']
