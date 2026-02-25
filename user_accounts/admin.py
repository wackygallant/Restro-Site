from django.contrib import admin
from .models import ShippingAddress

# Register your models here.
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('username', 'address', 'contact_no', 'city', 'created_at', 'updated_at')
    list_filter = ('city',)
    search_fields = ('username', 'address', 'contact_no', 'city')