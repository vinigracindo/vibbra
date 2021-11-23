from django.urls import path, include
from rest_framework import routers
from vibbra_ecommerce_api.invite import views

app_name = 'invite'

router = routers.DefaultRouter(trailing_slash=False)
router.register('invites', views.InviteViewSet, basename='invites')

urlpatterns = [
    path('users/<int:user_pk>/', include(router.urls)),
]
