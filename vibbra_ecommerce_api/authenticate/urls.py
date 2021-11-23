from django.urls import path, include
from rest_framework import routers
from vibbra_ecommerce_api.authenticate import views

app_name = 'auth'

router = routers.DefaultRouter(trailing_slash=False)
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('authenticate', views.TokenObtainPairView.as_view(), name='login'),
    path('authenticate/sso', views.SSOAuthView.as_view(), name='login-sso'),
    path('', include(router.urls)),
]
