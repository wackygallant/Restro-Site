from django.contrib import admin
from user_accounts.models import ShippingAddress, OTP

# Register your models here.
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('username', 'address', 'contact_no', 'city', 'created_at', 'updated_at')
    list_filter = ('city',)
    search_fields = ('username', 'address', 'contact_no', 'city')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'created_at')
    search_fields = ('email', 'otp')
    list_filter = ('created_at',)