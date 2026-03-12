from django.db import models

from order.models import Order

# Create your models here.
class Payment(models.Model):
    """Payment records for orders"""
    PAYMENT_METHODS = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('initiated', 'Initiated'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    pidx = models.CharField(max_length=100, null=True, blank=True)  # Khalti payment identifier
    payment_url = models.URLField(null=True, blank=True)  # For redirect URLs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def order_id(self):
        """Get order_id from related order"""
        return self.order.order_id
    
    def __str__(self):
        return f"Payment for {self.order_id} - {self.get_status_display()}"
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
