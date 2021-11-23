from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions, status
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from vibbra_ecommerce_api.authenticate.exceptions import Conflict
from vibbra_ecommerce_api.location.models import Location

from vibbra_ecommerce_api.location.serializer import LocationSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='first_name')
    login = serializers.CharField(source='username')
    location = LocationSerializer(many=False, read_only=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'login', 'password', 'location']

    def create(self, validated_data):
        location = validated_data.pop('location')
        location = Location.objects.create(**location)
        user = User.objects.create(**validated_data, location=location)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location')

        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.first_name = validated_data.get('first_name')
        instance.login = validated_data.get('login')
        instance.set_password(validated_data.get('password'))
        instance.save()

        data = {
            'lat': location_data.get('lat'),
            'lng': location_data.get('lng'),
            'address': location_data.get('address'),
            'city': location_data.get('city'),
            'state': location_data.get('state'),
            'zip_code': location_data.get('zip_code'),
        }

        if (instance.location):
            Location.objects.filter(pk=instance.location.pk).update(**data)
            instance.refresh_from_db()
        else:
            location = Location.objects.create(**data)
            instance.location = location
            instance.save()

        return instance


class SSOAuthSerializer(serializers.Serializer):
    app_token = serializers.CharField()
    login = serializers.CharField()


class TokenObtainSerializer(serializers.Serializer):
    username_field = 'login'

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['token'] = str(refresh.access_token)
        data['user'] = {
            'id': self.user.id,
            'name': self.user.get_full_name(),
            'email': self.user.email,
            'login': self.user.username
        }

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
