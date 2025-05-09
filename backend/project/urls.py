from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.sites.AdminSite.index_title = "Auth Server Platform administration"

schema_view = get_schema_view(
    openapi.Info(
        title="Auth Server",
        default_version="v1",
        description="",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    path(
        "api-docs<format>", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "api-docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

api_urlpatterns = [
    # path("", include(("apps.data_models.api.urls", "data_models"))),
]

django_views = []

urlpatterns = swagger_urlpatterns
urlpatterns += django_views
urlpatterns += [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("api/", include(api_urlpatterns)),
    path("", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


# ============================ STATIC CONFIG ================================ #
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
