from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from vibbra_ecommerce_api.invite.models import Invite
from vibbra_ecommerce_api.invite.serializer import InviteSerializer


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        invites = Invite.objects.filter(user=user_pk)
        return invites
