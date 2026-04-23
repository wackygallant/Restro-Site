from django.urls import path, include
from user_accounts.viewsets.user_profile import ProfileView, AddShippingAddressView, EditShippingAddressView, DeleteShippingAddressView
from customer_panel.viewsets.booking import AllBookingsView
from customer_panel.viewsets.order import AllOrdersView

urlpatterns = [
    path('user-profile/', include([
        path('', ProfileView.as_view(), name='profile'),
        path('all-bookings/', AllBookingsView.as_view(), name="all_bookings_page"),
        path('all-orders/', AllOrdersView.as_view(), name='all_orders' ),
        path('add-shipping-address/', AddShippingAddressView.as_view(), name='add_shipping_address'),
        path('edit-shipping-address/<int:pk>/', EditShippingAddressView.as_view(), name='edit_shipping_address'),
        path('delete-shipping-address/', DeleteShippingAddressView.as_view(), name='delete_shipping_address'),
    ])),
]
