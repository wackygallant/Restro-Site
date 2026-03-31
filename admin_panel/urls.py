from django.urls import path
from admin_panel.viewsets.admin_dashboard import DashboardView, LogoutView
from admin_panel.viewsets.admin_user import UserAdminView

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),
    path('users/', UserAdminView.as_view(), name='admin_users'),
]
