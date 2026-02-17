from django.contrib import admin
from order.models import Cart, CartItem, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'menu_item', 'quantity', 'created_at')
    search_fields = ('cart__user__username', 'menu_item__name')
    list_filter = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_amount', 'status')
    search_fields = ('user__username',)
    list_filter = ('status', 'order_date')
    readonly_fields = ('user', 'order_date')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'price')
    search_fields = ('order__user__username', 'menu_item__name')
    list_filter = ('order',)