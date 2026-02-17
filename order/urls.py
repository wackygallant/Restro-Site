from django.urls import path
from order.views import (
    OrderListView,
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView,
    CheckoutView
)

urlpatterns = [
    path('/', OrderListView.as_view(), name='orders'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/update/<int:cart_item_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
