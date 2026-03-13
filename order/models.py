from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItems
from django.db import models
import datetime

class OrderCart(models.Model):
    """Shopping cart for users before checkout"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='order_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderCart for {self.user.username}"
    
    def get_total_items(self):
        """Get total number of items in order cart"""
        return sum(item.quantity for item in self.order_cart_items.all())
    
    def get_total_price(self):
        """Get total price of all items in order cart"""
        return sum(item.get_total() for item in self.order_cart_items.all())

    class Meta:
        db_table = 'order_carts'
        verbose_name = 'Order Cart'
        verbose_name_plural = 'Order Carts'

class OrderCartItem(models.Model):
    """Items in the shopping cart"""
    #
    order_cart = models.ForeignKey(OrderCart, on_delete=models.CASCADE, related_name='order_cart_items')
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    def get_total(self):
        """Calculate total price for this order cart item"""
        if self.menu_item.is_on_special and self.menu_item.special_price:
            return self.menu_item.special_price * self.quantity
        return self.menu_item.price * self.quantity

    class Meta:
        db_table = 'order_cart_items'
        verbose_name = 'Order Cart Item'
        verbose_name_plural = 'Order Cart Items'
        unique_together = ('order_cart', 'menu_item')

class Order(models.Model):
    """Orders for users"""
    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shippingaddress = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.order_id} - {self.get_status_display()}"
    
    def calculate_total(self):
        """Calculate total price for this order"""
        total = sum(item.get_total() for item in self.order_items.all())
        self.total_amount = total
        self.save()
        return total

    def create_order_id(self):
        """Create a unique order ID in format ORD-YYYY-NNNN"""
        
        # Get current year
        current_year = datetime.datetime.now().year
        
        # Get the last order for this year to determine the next sequence number
        last_order = Order.objects.filter(
            order_id__startswith=f'ORD-{current_year}-'
        ).order_by('-order_id').first()
        
        if last_order:
            # Extract the sequence number from the last order ID
            last_sequence = int(last_order.order_id.split('-')[-1])
            next_sequence = last_sequence + 1
        else:
            next_sequence = 1
        
        # Format with leading zeros (4 digits)
        self.order_id = f'ORD-{current_year}-{next_sequence:04d}'
        return self.order_id

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    """Items in a completed order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItems, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name if self.menu_item else 'Deleted Item'}"
    
    def get_total(self):
        """Get total price for this order item"""
        return self.price * self.quantity

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'




