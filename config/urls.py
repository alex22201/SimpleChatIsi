from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/", include("apps.chat.urls")
    ),  # Assuming 'chat.urls' includes your API paths
    # Schema endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    # JWT Token endpoints
    path(
        "api/auth/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
