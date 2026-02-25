# Django Modules
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.conf import settings

# App Imports
from order.models import OrderCart, OrderCartItem, Order, OrderItem, Payment
from user_accounts.models import ShippingAddress
from menu.models import MenuItems
from utils._utils import get_username
from order.forms import CheckoutForm, PaymentVerificationForm, KhaltiPaymentForm

import time
import json
import requests


@method_decorator(login_required, name='dispatch')
class KhaltiPaymentVerificationView(View):
    """Handle Khalti payment verification after user returns from payment gateway"""
    def get(self, request):
        checkout_view = CheckoutView()
        return checkout_view.verify_khalti_payment(request)


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
    def get(self, request):
        """Display checkout page with shipping and payment options"""
        checkout_form = CheckoutForm()
        
        try:
            order_cart = OrderCart.objects.get(user=request.user)
            order_cart_items = order_cart.order_cart_items.all()
            shipping_addresses = ShippingAddress.objects.filter(username=request.user)
            
            if not order_cart_items.exists():
                messages.error(request, "Your order cart is empty!")
                return redirect('order_cart')
            
            if not shipping_addresses.exists():
                messages.error(request, "Please add a shipping address first!")
                return redirect('profile')
            
            # Populate shipping address choices
            shipping_choices = [(addr.id, addr) for addr in shipping_addresses]
            checkout_form.fields['shipping_address'].choices = shipping_choices
            
            context = {
                'form': checkout_form,
                'order_cart_items': order_cart_items,
                'shipping_addresses': shipping_addresses,
                'total_price': order_cart.get_total_price(),
            }
            return render(request, 'checkout.html', context)
            
        except OrderCart.DoesNotExist:
            messages.error(request, "Order cart not found!")
            return redirect('order_cart')

    def process_esewa_payment(self, request, order):
        """Process eSewa payment"""
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            payment_method='esewa',
            amount=order.total_amount,
            status='paid',
            transaction_id=f"esewa_{order.id}_{int(time.time())}"
        )
        
        # Clear order cart
        try:
            cart = OrderCart.objects.get(user=request.user)
            cart_items = cart.order_cart_items.all()
            print(f"Clearing {cart_items.count()} items from order cart for eSewa payment")
            cart_items.delete()
            print("Order cart cleared successfully for eSewa")
        except Exception as e:
            print(f"Error clearing order cart for eSewa: {e}")
            messages.error(request, "Error clearing order cart")
        
        messages.success(request, "Payment successful via eSewa!")
        return redirect('orders')
    
    def process_khalti_payment(self, request, order):
        """Process Khalti payment"""
        url = settings.KHALTI_API_URL
        initiate_url = url + "epayment/initiate/"
        secret_key = settings.KHALTI_SECRET_KEY

        # Create payment record with initiated status
        payment = Payment.objects.create(
            order=order,
            payment_method='khalti',
            amount=order.total_amount,
            status='initiated'
        )

        payload = {
            "return_url": request.build_absolute_uri('/orders'),
            "website_url": request.build_absolute_uri('/'),
            "amount": int(float(order.total_amount) * 100),  # Convert to paisa as integer
            "purchase_order_id": order.order_id,
            "purchase_order_name": "Restro Order",
            "customer_info": {
                "name": request.user.get_full_name() or request.user.username,
                "email": request.user.email or "customer@example.com",
                "phone": "9800000001"  # Default test phone, you may want to collect this from user
            }
        }
        headers = {
            'Authorization': f'key {secret_key}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(initiate_url, headers=headers, data=json.dumps(payload))
            
            # Log the response for debugging
            print(f"Khalti API Status Code: {response.status_code}")
            print(f"Khalti API Response: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"Parsed Response Data: {response_data}")
                
                # Update payment record with response data
                payment.pidx = response_data.get('pidx')
                payment.payment_url = response_data.get('payment_url')
                payment.save()
                
                # Khalti API returns payment_url directly for successful initiation
                payment_url = response_data.get('payment_url')
                if payment_url:
                    # Clear order cart
                    try:
                        cart = OrderCart.objects.get(user=payment.order.user)
                        cart_items = cart.order_cart_items.all()
                        print(f"Clearing {cart_items.count()} items from order cart for Khalti payment")
                        cart_items.delete()
                        print("Order cart cleared successfully for Khalti")
                    except Exception as e:
                        print(f"Error clearing order cart for Khalti: {e}")
                        messages.error(request, "Error clearing order cart")
                    
                    return redirect(payment_url)
                else:
                    error_message = response_data.get('message', 'Payment URL not received from Khalti')
                    print(f"Khalti Error: {error_message}")
                    payment.status = 'failed'
                    payment.save()
                    messages.error(request, f"Khalti payment initiation failed: {error_message}")
                    return redirect('checkout')
            else:
                print(f"Khalti API Error Response: {response.text}")
                payment.status = 'failed'
                payment.save()
                messages.error(request, f"Khalti API error: {response.status_code} - {response.text}")
                return redirect('checkout')
                
        except requests.exceptions.RequestException as e:
            payment.status = 'failed'
            payment.save()
            messages.error(request, f"Network error while connecting to Khalti: {str(e)}")
            return redirect('checkout')
        except Exception as e:
            payment.status = 'failed'
            payment.save()
            messages.error(request, f"Error processing Khalti payment: {str(e)}")
            return redirect('checkout')
    
    def post(self, request):
        """Process checkout with shipping and payment"""
        checkout_form = CheckoutForm(request.POST)
        
        if not checkout_form.is_valid():
            messages.error(request, "Please correct the errors below")
            return self.get(request)
        
        try:
            order_cart = OrderCart.objects.get(user=request.user)
            order_cart_items = order_cart.order_cart_items.all()
            
            if not order_cart_items.exists():
                messages.error(request, "Your order cart is empty!")
                return redirect('order_cart')
            
            # Get validated form data
            shipping_address_id = checkout_form.cleaned_data['shipping_address']
            payment_method = checkout_form.cleaned_data['payment_method']
            
            # Get shipping address
            shipping_address_obj = get_object_or_404(
                ShippingAddress, 
                id=shipping_address_id, 
                username=request.user
            )
            shipping_address = f"{shipping_address_obj.address}, {shipping_address_obj.city}"
            
            # Create order
            order = Order(
                user=request.user, 
                shippingaddress=shipping_address,
                status='completed'
            )
            order.create_order_id()
            order.save()
            
            # Create order items
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
            
            # Handle payment based on method
            if payment_method == 'cash_on_delivery':
                # Create cash on delivery payment record
                Payment.objects.create(
                    order=order,
                    payment_method='cash_on_delivery',
                    amount=order.total_amount,
                    status='pending'
                )
                messages.success(request, "Order placed successfully! Pay on delivery.")
            elif payment_method == 'esewa':
                return self.process_esewa_payment(request, order)
            elif payment_method == 'khalti':
                return self.process_khalti_payment(request, order)
            
            # Clear order cart for cash on delivery (eSewa and Khalti clear in their methods)
            if payment_method == 'cash_on_delivery':
                try:
                    cart_items = order_cart.order_cart_items.all()
                    print(f"Clearing {cart_items.count()} items from order cart for user {request.user.username}")
                    cart_items.delete()
                    print("Order cart cleared successfully")
                except Exception as e:
                    print(f"Error clearing order cart: {e}")
                    messages.error(request, "Error clearing order cart")
            
            return redirect('orders')
        
        except OrderCart.DoesNotExist:
            messages.error(request, "Order cart not found!")
            return redirect('order_cart')
        except ShippingAddress.DoesNotExist:
            messages.error(request, "Invalid shipping address!")
            return redirect('order_cart')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('order_cart')
