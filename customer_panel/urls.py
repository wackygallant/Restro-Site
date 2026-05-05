from django.urls import path, include

# View Imports
from customer_panel.viewsets.home import HomePage, AboutPage
from customer_panel.viewsets.booking import BookTableView
from customer_panel.viewsets.menu import Menu_Page, Menu_Item_Detail
from customer_panel.viewsets.order import OrderListView, OrderCartView, AddToOrderCartView, RemoveFromOrderCartView, UpdateOrderCartItemView, CheckoutView, PaymentVerificationView

urlpatterns = [
    # Home Pages
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),

    # Booking
    path('booking/', BookTableView.as_view(), name='booking_page'),
    
    # Menu
    path('menu/', include([
        path('', Menu_Page.as_view(), name='menu'),
        path('<slug:category_slug>/', Menu_Page.as_view(), name='category_filter'),
        path('item/<slug:item_slug>/', Menu_Item_Detail.as_view(), name='menu_item_detail'),
    ])),
    
    # Orders
    path('orders/', OrderListView.as_view(), name='orders'),

    # Cart
    path('cart/', include([
        path('', OrderCartView.as_view(), name='order_cart'),
        path('add/', AddToOrderCartView.as_view(), name='add_to_order_cart'),
        path('remove/<int:order_cart_item_id>/', RemoveFromOrderCartView.as_view(), name='remove_from_order_cart'),
        path('update/<int:order_cart_item_id>/', UpdateOrderCartItemView.as_view(), name='update_order_cart_item'),
    ])),
    
    # Checkout and Payment Verification
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment_verify/', PaymentVerificationView.as_view(), name="payment_verify")
]