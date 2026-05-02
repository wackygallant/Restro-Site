from django.urls import path, include
from admin_panel.viewsets.admin_dashboard import DashboardView, LogoutView
from admin_panel.viewsets.admin_payments import AdminPaymentEditView, PaymentListView
from admin_panel.viewsets.admin_user import UserAdminView, UserCreateView, UserEditView, UserDeleteView
from admin_panel.viewsets.admin_order import AdminOrderView, CompleteOrder, CancelOrder
from admin_panel.viewsets.admin_reservation import AdminReservationView
from admin_panel.viewsets.admin_menu import AdminMenuListView, AdminCategoryListView, AdminCategoryEditView, AdminCategoryDeleteView, AdminCategoryCreateView, AdminMenuCreateView, AdminMenuEditView, AdminMenuDeleteView
from admin_panel.viewsets.admin_reviews import AdminReviewsView, AdminReviewCreateView, AdminReviewEditView, AdminReviewDeleteView
from user_accounts.viewsets.auth import ChangePasswordView

urlpatterns = [
    path('', DashboardView.as_view(), name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='admin_logout'),

    # User Management
    path('users/', include([
        path('', UserAdminView.as_view(), name='admin_users'),
        path('create/', UserCreateView.as_view(), name='admin_user_create'),
        path('edit/<int:pk>/', UserEditView.as_view(), name='admin_user_edit'),
        path('delete/<int:pk>/', UserDeleteView.as_view(), name='admin_user_delete'),
    ])),
    
    # Order Management
    path('orders/', include([
        path('', AdminOrderView.as_view(), name='admin_orders'),
        path('complete/<int:order_id>/', CompleteOrder.as_view(), name='admin_order_complete'),
        path('cancel/<int:order_id>/', CancelOrder.as_view(), name='admin_order_cancel'),
    ])),
    
    # Reservation Management
    path('reservations/', AdminReservationView.as_view(), name='admin_reservations'),
    
    # Menu Management
    path('menu_categories/', include([
        path('', AdminCategoryListView.as_view(), name='admin_categories'),
        path('create/', AdminCategoryCreateView.as_view(), name='admin_category_create'),
        path('edit/<int:pk>/', AdminCategoryEditView.as_view(), name='admin_category_edit'),
        path('delete/<int:pk>/', AdminCategoryDeleteView.as_view(), name='admin_category_delete'),
    ])),

    path('menu_items/', include([
        path('', AdminMenuListView.as_view(), name='admin_menu'),
        path('create/', AdminMenuCreateView.as_view(), name='admin_menu_create'),
        path('edit/<int:pk>/', AdminMenuEditView.as_view(), name='admin_menu_edit'),
        path('delete/<int:pk>/', AdminMenuDeleteView.as_view(), name='admin_menu_delete'),
    ])),

    # Review Management
    path('reviews/', include([
        path('', AdminReviewsView.as_view(), name='admin_reviews'),
        path('create/', AdminReviewCreateView.as_view(), name='admin_review_create'),
        path('edit/<int:pk>/', AdminReviewEditView.as_view(), name='admin_review_edit'),
        path('delete/<int:pk>/', AdminReviewDeleteView.as_view(), name='admin_review_delete'),
    ])),
    path('payments/', include([ 
        path('', PaymentListView.as_view(), name='admin_payments'),
        path('edit/<int:pk>/', AdminPaymentEditView.as_view(), name='admin_payment_edit'),
    ])),
]
