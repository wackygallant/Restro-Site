from django.contrib import admin
from order.models import OrderCart, OrderCartItem, Order, OrderItem

@admin.register(OrderCart)
class OrderCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderCartItem)
class OrderCartItemAdmin(admin.ModelAdmin):
    list_display = ('order_cart', 'menu_item', 'quantity', 'created_at')
    search_fields = ('order_cart__user__username', 'menu_item__name')
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