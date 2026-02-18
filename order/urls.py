from django.urls import path
from order.views import (
    OrderListView,
    OrderCartView,
    AddToOrderCartView,
    RemoveFromOrderCartView,
    UpdateOrderCartItemView,
    CheckoutView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='orders'),
    path('order_cart/', OrderCartView.as_view(), name='order_cart'),
    path('order_cart/add/', AddToOrderCartView.as_view(), name='add-to-order-cart'),
    path('order_cart/remove/<int:order_cart_item_id>/', RemoveFromOrderCartView.as_view(), name='remove-from-order-cart'),
    path('order_cart/update/<int:order_cart_item_id>/', UpdateOrderCartItemView.as_view(), name='update-order-cart-item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
