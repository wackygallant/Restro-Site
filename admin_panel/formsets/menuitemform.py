from django import forms
from menu.models import MenuItems

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItems
        fields = ['slug', 'name', 'category', 'description', 'price', 'image', 'is_on_special', 'special_price']