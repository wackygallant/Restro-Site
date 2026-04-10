from django.urls import path
from admin_panel.viewsets.admin_dashboard import DashboardView, LogoutView
from admin_panel.viewsets.admin_user import UserAdminView, UserCreateView, UserEditView, UserDeleteView
from admin_panel.viewsets.admin_order import AdminOrderView, CompleteOrder, CancelOrder
from admin_panel.viewsets.admin_reservation import AdminReservationView
from admin_panel.viewsets.admin_menu import AdminMenuListView, AdminCategoryListView, AdminCategoryEditView, AdminCategoryDeleteView, AdminCategoryCreateView, AdminMenuCreateView, AdminMenuEditView, AdminMenuDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),

    # User Management
    path('users/', UserAdminView.as_view(), name='admin_users'),
    path('users/create/', UserCreateView.as_view(), name='admin_user_create'),
    path('users/edit/<int:pk>/', UserEditView.as_view(), name='admin_user_edit'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),
    
    # Order Management
    path('orders/', AdminOrderView.as_view(), name='admin_orders'),
    path('orders/complete/<int:order_id>/', CompleteOrder.as_view(), name='admin_order_complete'),
    path('orders/cancel/<int:order_id>/', CancelOrder.as_view(), name='admin_order_cancel'),
    
    # Reservation Management
    path('reservations/', AdminReservationView.as_view(), name='admin_reservations'),
    
    # Menu Management
    path('menu-categories/', AdminCategoryListView.as_view(), name='admin_categories'),
    path('menu-categories/create/', AdminCategoryCreateView.as_view(), name='admin_category_create'),
    path('menu-categories/edit/<int:pk>/', AdminCategoryEditView.as_view(), name='admin_category_edit'),
    path('menu-categories/delete/<int:pk>/', AdminCategoryDeleteView.as_view(), name='admin_category_delete'),
    path('menu-items/', AdminMenuListView.as_view(), name='admin_menu'),
    path('menu-items/create/', AdminMenuCreateView.as_view(), name='admin_menu_create'),
    path('menu-items/edit/<int:pk>/', AdminMenuEditView.as_view(), name='admin_menu_edit'),
    path('menu-items/delete/<int:pk>/', AdminMenuDeleteView.as_view(), name='admin_menu_delete'),
]
