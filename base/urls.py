from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from base import settings
from common.views import LogAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Trello API",
        default_version='v1',
        description="Trello API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@trello.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
    urlconf='base.urls',
)

urlpatterns = [
    path('', include('common.urls')),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/logs/', LogAPIView.as_view(), name='log-api'),
    path('api/', include('user_control.urls')),
    path('api/', include('workspace_control.urls')),
    path('api/', include('board_control.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
