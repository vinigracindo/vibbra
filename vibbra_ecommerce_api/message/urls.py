from django.urls import path, include
from rest_framework import routers
from vibbra_ecommerce_api.message import views

app_name = 'message'

router = routers.DefaultRouter(trailing_slash=False)
router.register('messages', views.MessageViewSet, basename='Message')

urlpatterns = [
    path('deals/<int:deal_pk>/', include(router.urls)),
]
