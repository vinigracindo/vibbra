from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Vibbra e-commerce API",
        default_version='v1',
        description="Documentação da API",
        terms_of_service="#",
        contact=openapi.Contact(email="vini.gracindo@gmail.com"),
        license=openapi.License(name="Vibbra License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/', include('vibbra_ecommerce_api.core.urls'), name='auth'),
    path('api/v1/', include('vibbra_ecommerce_api.authenticate.urls'), name='auth'),
    path('api/v1/', include('vibbra_ecommerce_api.message.urls'), name='message'),
    path('api/v1/', include('vibbra_ecommerce_api.invite.urls'), name='invite'),
    path('admin/', admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc",
         cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
