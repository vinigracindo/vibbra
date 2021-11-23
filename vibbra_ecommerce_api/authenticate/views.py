from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from vibbra_ecommerce_api.authenticate.exceptions import Conflict
from drf_yasg.utils import swagger_auto_schema

from vibbra_ecommerce_api.authenticate.serializer import SSOAuthSerializer, TokenObtainPairSerializer, UserSerializer
from rest_framework import status, viewsets

User = get_user_model()


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer


class SSOAuthView(APIView):
    @swagger_auto_schema(request_body=SSOAuthSerializer)
    def post(self, request):
        serializer = SSOAuthSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.data['login']
            app_token = serializer.data['app_token']
            try:
                user = User.objects.get(username=login)
                if not Token.objects.filter(user=user, key=app_token).exists():
                    error = {'error': 'invalid token for this login'}
                else:
                    refresh = RefreshToken.for_user(user)
                    response = {'token': str(
                        refresh.access_token), 'user': {
                        'id': user.id,
                        'name': user.get_full_name(),
                        'email': user.email,
                        'login': user.username
                    }}
                    return Response(response, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                error = {'error': 'invalid login'}
        else:
            error = {'error': serializer.errors}
        return Response(error, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put']

    def create(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data['login']).exists():
            raise Conflict('The login already exists.', 'user_already_exists')
        return super(UserViewSet, self).create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if User.objects.exclude(pk=instance.pk).filter(username=request.data['login']).exists():
            raise Conflict('The login already exists.', 'user_already_exists')
        return super(UserViewSet, self).update(request, args, kwargs)
