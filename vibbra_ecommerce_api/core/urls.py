from django.urls import path, include
from rest_framework import routers
from vibbra_ecommerce_api.core import views

app_name = 'core'

deals_router = routers.DefaultRouter(trailing_slash=False)
deals_router.register('deals', views.DealViewSet, basename='deals')

bids_router = routers.DefaultRouter(trailing_slash=False)
bids_router.register('bids', views.BidViewSet, basename="bids")

urlpatterns = [
    path('', include(deals_router.urls)),
    path('deals/<int:deal_pk>/', include(bids_router.urls)),
    path('deal/<int:deal_pk>/deliveries', views.deliveries, name='deliveries'),
]
