from django.views import View
from django.shortcuts import render

from utils import _utils

from .models import MenuCategories, MenuItems

class Menu_Page(View):
    def get(self, request, category_slug=None):
        username = _utils.get_username(request)
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
        username = _utils.get_username(request)
        menu_item = MenuItems.objects.get(slug=item_slug)
        context = {
            "menu_item": menu_item,
            "username": username
        }
        return render(request, "menu_item.html", context)