from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages

from utils._utils import get_username

from menu.models import MenuCategories, MenuItems


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
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to add items to cart.")
            return redirect('login')
        
        item = MenuItems.objects.get(slug=item_slug)
        quantity_str = request.POST.get('quantity', '1').strip()
        quantity = int(quantity_str) if quantity_str else 1

        # Add to cart instead of creating an order item
        from order.models import Cart, CartItem
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Item already in cart, increase quantity
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f"Added {quantity}x {item.name} to your cart!")
        return redirect('orders')   