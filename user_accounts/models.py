# Django Module Imports
from django.db import models
from django.utils import timezone

# Python Package Imports
from datetime import timedelta

# Custom Util Imports
from utils.models import BaseModel

class ShippingAddress(models.Model):
    username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.address
    
    class Meta:
        db_table = 'shipping_addresses'
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

class OTP(BaseModel):
    email = models.EmailField()
    otp = models.CharField(max_length=6)

    def is_active(self):
        # Valid for only 5 minutes
        return timezone.now() < self.created_at + timedelta(minutes=5)
    
    def __str__(self):
        return f"{self.email} - {self.otp}"
    
    class Meta:
        db_table = 'otp'
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'