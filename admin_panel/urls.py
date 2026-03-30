from django.urls import path
from admin_panel.viewsets.dashboard import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
]
