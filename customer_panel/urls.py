from django.urls import path

# View Imports
from customer_panel.viewsets.custom_pages import HomePage, AboutPage
from customer_panel.viewsets.booking import BookTableView
from customer_panel.viewsets.menu import Menu_Page, Menu_Item_Detail
from customer_panel.viewsets.order import OrderListView, OrderCartView, AddToOrderCartView, RemoveFromOrderCartView, UpdateOrderCartItemView, CheckoutView

urlpatterns = [
    # Home Pages
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),

    # Booking
    path('booking/', BookTableView.as_view(), name='booking_page'),
    
    # Menu
    path('menu/all/', Menu_Page.as_view(), name='menu'),
    path('menu/<slug:category_slug>/', Menu_Page.as_view(), name='category_filter'),
    path('menu/item/<slug:item_slug>/', Menu_Item_Detail.as_view(), name='menu_item_detail'),
    
    # Orders
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/order_cart/', OrderCartView.as_view(), name='order_cart'),
    path('orders/order_cart/add/', AddToOrderCartView.as_view(), name='add-to-order-cart'),
    path('orders/order_cart/remove/<int:order_cart_item_id>/', RemoveFromOrderCartView.as_view(), name='remove-from-order-cart'),
    path('orders/order_cart/update/<int:order_cart_item_id>/', UpdateOrderCartItemView.as_view(), name='update-order-cart-item'),
    path('orders/checkout/', CheckoutView.as_view(), name='checkout'),
    ]