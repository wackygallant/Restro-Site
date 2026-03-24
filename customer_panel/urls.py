from django.urls import path

from customer_panel.viewsets.custom_pages import HomePage, AboutPage
from customer_panel.viewsets.booking import BookTableView
from customer_panel.viewsets.menu import Menu_Page, Menu_Item_Detail
from customer_panel.viewsets.order import OrderListView, OrderCartView, AddToOrderCartView, RemoveFromOrderCartView, UpdateOrderCartItemView, CheckoutView
from customer_panel.viewsets.user_accounts import LoginView, LogoutView, RegisterView, ProfileView, AddShippingAddressView, EditShippingAddressView, DeleteShippingAddressView
from customer_panel.viewsets.booking import AllBookingsView
from customer_panel.viewsets.order import AllOrdersView

urlpatterns = [
    # Home Pages
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),

    # User Accounts
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', ProfileView.as_view(), name='profile'),
    path('user/all-bookings/', AllBookingsView.as_view(), name="all_bookings_page"),
    path('user/all-orders/', AllOrdersView.as_view(), name='all_orders' ),
    path('user/add-shipping-address/', AddShippingAddressView.as_view(), name='add_shipping_address'),
    path('user/edit-shipping-address/<int:pk>/', EditShippingAddressView.as_view(), name='edit_shipping_address'),
    path('user/delete-shipping-address/', DeleteShippingAddressView.as_view(), name='delete_shipping_address'),

    # Booking
    path('booking/', BookTableView.as_view(), name='booking_page'),
    # Menu
    path('menu/', Menu_Page.as_view(), name='menu'),
    path('menu/category/<slug:category_slug>/', Menu_Page.as_view(), name='category_filter'),
    path('menu/item/<slug:item_slug>/', Menu_Item_Detail.as_view(), name='menu_item_detail'),
    # Orders
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/order_cart/', OrderCartView.as_view(), name='order_cart'),
    path('orders/order_cart/add/', AddToOrderCartView.as_view(), name='add-to-order-cart'),
    path('orders/order_cart/remove/<int:order_cart_item_id>/', RemoveFromOrderCartView.as_view(), name='remove-from-order-cart'),
    path('orders/order_cart/update/<int:order_cart_item_id>/', UpdateOrderCartItemView.as_view(), name='update-order-cart-item'),
    path('orders/checkout/', CheckoutView.as_view(), name='checkout'),
    ]