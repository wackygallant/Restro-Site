from django.urls import path
from admin_panel.viewsets.admin_dashboard import DashboardView, LogoutView
from admin_panel.viewsets.admin_user import UserAdminView, UserCreateView, UserEditView, UserDeleteView
from admin_panel.viewsets.admin_order import AdminOrderView, AdminOrderItemsView

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),
    path('users/', UserAdminView.as_view(), name='admin_users'),
    path('users/create/', UserCreateView.as_view(), name='admin_user_create'),
    path('users/edit/<int:pk>/', UserEditView.as_view(), name='admin_user_edit'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),
    path('orders/', AdminOrderView.as_view(), name='admin_orders'),
    path('orders/<int:order_id>/', AdminOrderItemsView.as_view(), name='admin_order_items'),
]
