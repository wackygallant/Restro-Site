from django.contrib import admin

from order.models import Orders, OrderItems

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'order_date', 'total_amount')
    search_fields = ('order_number', 'customer_name')
    list_filter = ('order_date',)

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('menu_item_name', 'quantity', 'price')
    search_fields = ('menu_item_name',)
    list_filter = ('menu_item_name',)