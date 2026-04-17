from django.contrib import admin
from django.urls import include, path
from . import settings
from django.conf.urls.static import static
from user_accounts.viewsets.auth import LoginView, LogoutView, RegisterView, PasswordResetView

urlpatterns = [
    path('default-admin/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('', include('customer_panel.urls')),
    path('', include('user_accounts.urls')),
    path('api/', include('api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)