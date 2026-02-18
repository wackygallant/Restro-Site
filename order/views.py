from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from order.models import OrderCart, OrderCartItem, Order, OrderItem
from menu.models import MenuItems
from utils._utils import get_username

class OrderListView(View):
    """Display user's order cart (repurposed as the orders page)"""
    def get(self, request):
        username = get_username(request)
        order_cart_items = []
        total_price = 0
        
        if request.user.is_authenticated:
            order_cart, created = OrderCart.objects.get_or_create(user=request.user)
            order_cart_items = order_cart.order_cart_items.all()
            total_price = order_cart.get_total_price()
        
        return render(request, 'orders.html', {
            'order_cart_items': order_cart_items,
            'total_price': total_price,
            'username': username
        })

@method_decorator(login_required, name='dispatch')
class OrderCartView(View):
    """Display user's shopping order cart"""
    def get(self, request):
        order_cart, created = OrderCart.objects.get_or_create(user=request.user)
        order_cart_items = order_cart.order_cart_items.all()
        total_items = order_cart.get_total_items()
        total_price = order_cart.get_total_price()
        
        return render(request, 'orders.html', {
            'order_cart': order_cart,
            'order_cart_items': order_cart_items,
            'total_items': total_items,
            'total_price': total_price
        })

@method_decorator(login_required, name='dispatch')
class AddToOrderCartView(View):
    """Add item to order cart"""
    def post(self, request):
        menu_item_id = request.POST.get('menu_item_id')
        quantity_str = request.POST.get('quantity', '1').strip()
        quantity = int(quantity_str) if quantity_str else 1
        
        menu_item = get_object_or_404(MenuItems, id=menu_item_id)
        order_cart, created = OrderCart.objects.get_or_create(user=request.user)
        
        order_cart_item, created = OrderCartItem.objects.get_or_create(
            order_cart=order_cart,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Item already in order cart, increase quantity
            order_cart_item.quantity += quantity
            order_cart_item.save()
        
        messages.success(request, f"{menu_item.name} added to order cart!")
        return redirect('orders')

@method_decorator(login_required, name='dispatch')
class RemoveFromOrderCartView(View):
    """Remove item from order cart"""
    def post(self, request, order_cart_item_id):
        order_cart_item = get_object_or_404(OrderCartItem, id=order_cart_item_id, order_cart__user=request.user)
        menu_item_name = order_cart_item.menu_item.name
        order_cart_item.delete()
        messages.success(request, f"{menu_item_name} removed from order cart!")
        return redirect('order_cart')

@method_decorator(login_required, name='dispatch')
class UpdateOrderCartItemView(View):
    """Update quantity of item in order cart"""
    def post(self, request, order_cart_item_id):
        quantity_str = request.POST.get('quantity', '1').strip()
        quantity = int(quantity_str) if quantity_str else 1
        order_cart_item = get_object_or_404(OrderCartItem, id=order_cart_item_id, order_cart__user=request.user)
        
        if quantity > 0:
            order_cart_item.quantity = quantity
            order_cart_item.save()
            messages.success(request, "Order cart updated!")
        else:
            order_cart_item.delete()
            messages.success(request, "Item removed from order cart!")
            
        return redirect('order_cart')

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    """Convert order cart to order"""
    def post(self, request):
        try:
            order_cart = OrderCart.objects.get(user=request.user)
            order_cart_items = order_cart.order_cart_items.all()
            
            if not order_cart_items.exists():
                messages.error(request, "Your order cart is empty!")
                return redirect('order_cart')
            
            # Create a new order for this checkout
            order = Order.objects.create(user=request.user)
            
            # Create order items from order cart items
            for order_cart_item in order_cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=order_cart_item.menu_item,
                    quantity=order_cart_item.quantity,
                    price=order_cart_item.menu_item.special_price if (
                        order_cart_item.menu_item.is_on_special and order_cart_item.menu_item.special_price
                    ) else order_cart_item.menu_item.price
                )
            
            # Calculate total
            order.calculate_total()
            
            # Clear order cart
            order_cart.order_cart_items.all().delete()
            
            messages.success(request, "Order placed successfully!")
            return redirect('orders')
        
        except OrderCart.DoesNotExist:
            messages.error(request, "Order cart not found!")
            return redirect('order_cart')