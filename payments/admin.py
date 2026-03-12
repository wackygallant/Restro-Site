from django.contrib import admin

from payments.models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order', 'payment_method', 'amount', 'status', 'transaction_id', 'created_at')
    search_fields = ('order_id', 'order__user__username', 'transaction_id', 'pidx')
    list_filter = ('payment_method', 'status', 'created_at')
    readonly_fields = ('order_id', 'order', 'payment_method', 'amount', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'order__user')