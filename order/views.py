from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from order.models import Cart, CartItem, Order, OrderItem
from menu.models import MenuItems
from utils._utils import get_username

class OrderListView(View):
    """Display user's cart (repurposed as the orders page)"""
    def get(self, request):
        username = get_username(request)
        cart_items = []
        total_price = 0
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.cart_items.all()
            total_price = cart.get_total_price()
        
        return render(request, 'orders.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'username': username
        })

@method_decorator(login_required, name='dispatch')
class CartView(View):
    """Display user's shopping cart"""
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cart_items.all()
        total_items = cart.get_total_items()
        total_price = cart.get_total_price()
        
        return render(request, 'orders.html', {
            'cart': cart,
            'cart_items': cart_items,
            'total_items': total_items,
            'total_price': total_price
        })

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    """Add item to cart"""
    def post(self, request):
        menu_item_id = request.POST.get('menu_item_id')
        quantity_str = request.POST.get('quantity', '1').strip()
        quantity = int(quantity_str) if quantity_str else 1
        
        menu_item = get_object_or_404(MenuItems, id=menu_item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Item already in cart, increase quantity
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f"{menu_item.name} added to cart!")
        return redirect('orders')

@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    """Remove item from cart"""
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        menu_item_name = cart_item.menu_item.name
        cart_item.delete()
        messages.success(request, f"{menu_item_name} removed from cart!")
        return redirect('cart')

@method_decorator(login_required, name='dispatch')
class UpdateCartItemView(View):
    """Update quantity of item in cart"""
    def post(self, request, cart_item_id):
        quantity_str = request.POST.get('quantity', '1').strip()
        quantity = int(quantity_str) if quantity_str else 1
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated!")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart!")
            
        return redirect('cart')

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    """Convert cart to order"""
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cart_items.all()
            
            if not cart_items.exists():
                messages.error(request, "Your cart is empty!")
                return redirect('cart')
            
            # Create a new order for this checkout
            order = Order.objects.create(user=request.user)
            
            # Create order items from cart items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity,
                    price=cart_item.menu_item.special_price if (
                        cart_item.menu_item.is_on_special and cart_item.menu_item.special_price
                    ) else cart_item.menu_item.price
                )
            
            # Calculate total
            order.calculate_total()
            
            # Clear cart
            cart.cart_items.all().delete()
            
            messages.success(request, "Order placed successfully!")
            return redirect('orders')
        
        except Cart.DoesNotExist:
            messages.error(request, "Cart not found!")
            return redirect('cart')