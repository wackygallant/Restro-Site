from django.urls import path
import order.views

urlpatterns = [
    path('', order.views.OrderListView.as_view(), name='orders'),
    path('order_cart/', order.views.OrderCartView.as_view(), name='order_cart'),
    path('order_cart/add/', order.views.AddToOrderCartView.as_view(), name='add-to-order-cart'),
    path('order_cart/remove/<int:order_cart_item_id>/', order.views.RemoveFromOrderCartView.as_view(), name='remove-from-order-cart'),
    path('order_cart/update/<int:order_cart_item_id>/', order.views.UpdateOrderCartItemView.as_view(), name='update-order-cart-item'),
    path('checkout/', order.views.CheckoutView.as_view(), name='checkout'),
]
