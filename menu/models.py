from django.db import models

from utils.models import BaseModel, CommonModel

class MenuCategories(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"

class MenuItems(CommonModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(MenuCategories, on_delete=models.CASCADE, related_name='menu_items')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    is_on_special = models.BooleanField(default=False)
    special_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
