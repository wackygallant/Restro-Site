from django.contrib import admin
from django.urls import include, path
from core import settings
from django.conf.urls.static import static
from user_accounts.viewsets.auth import LoginView, LogoutView, RegisterView, PasswordResetView

urlpatterns = [
    path('default-admin/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('', include('customer_panel.urls')),
    path('', include('user_accounts.urls')),
]

# Static and Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Swagger UI
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/', include([
        path("", include('api.urls')),
        # YOUR PATTERNS
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='doc'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]