
from django.urls import path
from user_accounts.viewsets.auth import LoginView, LogoutView, RegisterView, PasswordResetView
from user_accounts.viewsets.user_profile import ProfileView, AddShippingAddressView, EditShippingAddressView, DeleteShippingAddressView
from customer_panel.viewsets.booking import AllBookingsView
from customer_panel.viewsets.order import AllOrdersView

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),

    # User Accounts
    path('user-profile/', ProfileView.as_view(), name='profile'),
    path('user-profile/all-bookings/', AllBookingsView.as_view(), name="all_bookings_page"),
    path('user-profile/all-orders/', AllOrdersView.as_view(), name='all_orders' ),
    path('user-profile/add-shipping-address/', AddShippingAddressView.as_view(), name='add_shipping_address'),
    path('user-profile/edit-shipping-address/<int:pk>/', EditShippingAddressView.as_view(), name='edit_shipping_address'),
    path('user-profile/delete-shipping-address/', DeleteShippingAddressView.as_view(), name='delete_shipping_address'),
]
