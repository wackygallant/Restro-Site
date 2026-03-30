from django.urls import path
from admin_panel.viewsets.dashboard import DashboardView, LogoutView

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),
]
