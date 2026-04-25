from django.db import models
from utils.models import BaseModel

from order.models import Order

class Payment(BaseModel):
    """Payment records for orders"""
    PAYMENT_METHODS = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)  # Khalti payment identifier
    
    @property
    def order_id(self):
        """Get order_id from related order"""
        return self.order.order_id
    
    def __str__(self):
        return f"Payment for {self.order_id} - {self.status}"
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'