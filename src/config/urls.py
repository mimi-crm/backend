from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

#
# from config.views import ReactAppView

base_url = "api/v1"

urlpatterns = [
    path(f"{base_url}/admin/", admin.site.urls),
    path(f"{base_url}/oauth/", include("oauth.urls")),
    path(f"{base_url}/users/", include("users.urls")),
    path(f"{base_url}/customers/", include("customers.urls")),
    path(f"{base_url}/counsels/", include("counsels.urls")),
    # path("", ReactAppView.as_view(), name="react-app"),
    path("", TemplateView.as_view(template_name="index.html")),  # React 빌드 파일 서빙
]

if settings.DEBUG:
    urlpatterns += [
        path(f"{base_url}/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            f"{base_url}/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            f"{base_url}/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
