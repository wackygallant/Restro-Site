from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages

from utils._utils import get_username

from menu.models import MenuCategories, MenuItems
from order.models import Orders, OrderItems


class Menu_Page(View):
    def get(self, request, category_slug=None):
        username = get_username(request)
        categories = MenuCategories.objects.all().order_by('priority')
        if category_slug:  # If user clicked a category
            filtered_menu_items = MenuItems.objects.filter(
            category__slug=category_slug
            )
        else:
            filtered_menu_items = MenuItems.objects.all()
        context = {
            "options": categories,
            "filtered_menu_items": filtered_menu_items,
            "username": username
        }
        return render(request, "menu.html", context)

    
class Menu_Item_Detail(View):
    def get(self, request, item_slug):
        username = get_username(request)
        menu_item = MenuItems.objects.get(slug=item_slug)
        context = {
            "menu_item": menu_item,
            "username": username
        }
        return render(request, "menu_item.html", context)
    
    def post(self, request, item_slug):
        item = MenuItems.objects.get(slug=item_slug)
        quantity = int(request.POST.get('quantity', 1))
        calculated_price = item.price * quantity

        OrderItems.objects.create(
            menu_item_name=item.name,
            quantity=quantity,
            price=calculated_price
        )

        # 1. Add the success message
        messages.success(request, f"Added {quantity}x {item.name} to your order!")

        # 2. Redirect to avoid duplicate submissions on refresh
        return redirect('order-list')    