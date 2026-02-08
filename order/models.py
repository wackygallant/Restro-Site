from django.db import models

class Orders(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_number} by {self.customer_name}"
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItems(models.Model):
    menu_item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item_name}"
    
    def get_total_amount(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total
    
    class Meta: 
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


