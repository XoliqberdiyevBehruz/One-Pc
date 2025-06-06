from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="OnePc API",
      default_version='v1',
      description="OnePc description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="xoliqberdiyevbehruz12@gmail.com"),
      license=openapi.License(name="OnePc License"),
   ),
   public=True,
   url='https://pc.onepc.uz'
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('api/v1/common/', include('common.urls')),
    path('api/v1/product/', include('product.urls')),
    # swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += i18n_patterns(
    path('set_languages/', include('django.conf.urls.i18n')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
