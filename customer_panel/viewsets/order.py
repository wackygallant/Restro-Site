# Django Modules Import
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View, generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db import transaction

# App Imports
from order.models import OrderCart, OrderCartItem, Order, OrderItem
from payments.models import Payment
from user_accounts.models import ShippingAddress
from menu.models import MenuItems
from customer_panel.formsets.orderform import CheckoutForm

# Custom Util Imports
from utils._utils import get_username

# Python Package Imports
import time
import requests
import json
import base64
import hashlib
import hmac


class AllOrdersView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name="customer_panel/all_orders.html"
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-order_date')

class OrderListView(LoginRequiredMixin, View):
    """Display user's order cart"""
    def get(self, request):
        username = get_username(request)
        order_cart_items = []
        total_price = 0
        
        if request.user.is_authenticated:
            order_cart, created = OrderCart.objects.get_or_create(user=request.user)
            order_cart_items = order_cart.order_cart_items.all()
            total_price = order_cart.get_total_price()
        
        return render(request, 'customer_panel/cart.html', {
            'order_cart_items': order_cart_items,
            'total_price': total_price,
            'username': username
        })

class OrderCartView(LoginRequiredMixin, View):
    """Display user's shopping order cart"""
    def get(self, request):
        order_cart, created = OrderCart.objects.get_or_create(user=request.user)
        order_cart_items = order_cart.order_cart_items.all()
        total_items = order_cart.get_total_items()
        total_price = order_cart.get_total_price()
        
        return render(request, 'customer_panel/cart.html', {
            'order_cart': order_cart,
            'order_cart_items': order_cart_items,
            'total_items': total_items,
            'total_price': total_price
        })

class AddToOrderCartView(LoginRequiredMixin, View):
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

class RemoveFromOrderCartView(LoginRequiredMixin, View):
    """Remove item from order cart"""
    def post(self, request, order_cart_item_id):
        order_cart_item = get_object_or_404(OrderCartItem, id=order_cart_item_id, order_cart__user=request.user)
        menu_item_name = order_cart_item.menu_item.name
        order_cart_item.delete()
        messages.success(request, f"{menu_item_name} removed from order cart!")
        return redirect('order_cart')

class UpdateOrderCartItemView(LoginRequiredMixin, View):
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

class PaymentVerificationView(LoginRequiredMixin,generic.TemplateView):
    template_name = "customer_panel/payment_verify.html"

    def handle_khalti_payment_verification(self, request, order): # Ensure 'order' is passed in
        params = request.GET.dict()
        pidx = params.get("pidx", "")
        purchase_order_id = params.get("purchase_order_id", "")

        payment_details = Payment.objects.filter(transaction_id=purchase_order_id).first()

        if not payment_details:
            # If we can't find the payment, we can't find the order safely
            messages.error(request, "Payment record not found.")
            return redirect("orders")
        
        # Ensure we are working with the correct order object
        order = payment_details.order
        
        verify_url = f"{settings.KHALTI_API_URL}epayment/lookup/"
        headers = {
            "Authorization": f"Key {settings.KHALTI_API_SECRET_KEY}",  
            'Content-Type': 'application/json',
        }  

        try:
            response = requests.post(verify_url, headers=headers, json={"pidx": pidx}, timeout=10)
            response_data = response.json()
        except Exception as e:
            # Handle Timeout or Connection Error
            order.order_status = 'failed'
            order.save()
            messages.error(request, "Communication error with Khalti.")
            return redirect("orders")

        if response.status_code == 200 and response_data.get("status") == "Completed":
            # SUCCESS PATH
            payment_details.status = "paid"
            payment_details.save()
            
            order.order_status = 'completed' # Standardize field names (status vs order_status)
            order.save()

            # Clear cart logic...
            messages.success(request, "Payment successful via Khalti!")
            return redirect('orders')
        
        else:
            # FAILURE PATH (API returned 400/500 or status was 'Expired/Canceled')
            payment_details.status = "failed"
            payment_details.save()

            order.order_status = 'failed'
            order.save()
            
            error_msg = response_data.get("detail", "Payment was not completed.")
            messages.error(request, f"Khalti Error: {error_msg}")
            return redirect("orders")

    def handle_esewa_payment_verification(self, request):
        params = request.GET.dict()
        data = params.get("data", "")
        
        decoded_message = base64.b64decode(data)
        json_data = json.loads(decoded_message)

        total_amount = json_data.get("total_amount")
        transaction_uuid = json_data.get("transaction_uuid")
        status_check_url = f"https://rc.esewa.com.np/api/epay/transaction/status/?product_code={settings.ESEWA_MERCHANT_ID}&total_amount={total_amount}&transaction_uuid={transaction_uuid}"
        response = requests.get(status_check_url)

        if response.status_code == 200:
            response = response.json()
            payment_details = Payment.objects.filter(payment_id=transaction_uuid).first()

            if response['status'] == "COMPLETE":
                # Update Payment Record
                payment_details.status = "paid"
                payment_details.save()
                
                # Update Related Order Status if necessary
                order = payment_details.order
                order.status = 'completed'
                order.save()

                # Clear order cart
                try:
                    cart = OrderCart.objects.get(user=request.user)
                    cart.order_cart_items.all().delete()
                except Exception as e:
                    print(f"Cart clearing error: {e}")
                messages.success(request, "Payment successful via Esewa!")
                return redirect('orders')

            else:
                # FAILURE PATH (API returned 400/500 or status was 'Expired/Canceled')
                payment_details.status = "failed"
                payment_details.save()

                order.order_status = 'failed'
                order.save()
                
                error_msg = response_data.get("detail", "Payment was not completed.")
                messages.error(request, f"Khalti Error: {error_msg}")
                return redirect("orders")

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        purchase_order_id = params.get('purchase_order_id', '')

        try:
            with transaction.atomic():
                if "pidx" in params or "khalti" in purchase_order_id.lower():
                    return self.handle_khalti_payment_verification(request)
                else:
                    return self.handle_esewa_payment_verification(request)

        except Exception as e:
            print(f"Error in verification: {e}")
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect("orders")

class CheckoutView(LoginRequiredMixin, View):        
    def process_cod(self, request, order):
        # Create cash on delivery payment record
        Payment.objects.create(
            order=order,
            payment_method='cash_on_delivery',
            amount=order.total_amount,
            status='pending'
        )

        # Clear order cart
        try:
            cart = OrderCart.objects.get(user=request.user)
            cart_items = cart.order_cart_items.all()
            print(f"Clearing {cart_items.count()} items from order cart for eSewa payment")
            cart_items.delete()
            print("Order cart cleared successfully.")
        except Exception as e:
            print(f"Error clearing order cart: {e}")
            messages.error(request, "Error clearing order cart")
        
        messages.success(request, "Order placed successfully! Pay on delivery.")
        return redirect('orders')
    
    def initiate_khalti_payment(self, request, order):
        url = settings.KHALTI_API_URL
        secret_key = settings.KHALTI_API_SECRET_KEY

        if not url or not secret_key:
            return redirect(request.path)

        initiate_url = f"{url}epayment/initiate/"

        # 1. Create a unique internal transaction ID first
        unique_txn_id = f"KHALTI_{order.id}_{int(time.time())}"

        headers = {
            'Authorization': f'Key {secret_key}',
            'Content-Type': 'application/json',
        }

        # 2. Dynamic Payload (Amount in Paisa)
        payload_dict = {
            "return_url": "http://localhost:8000/payment_verify/",
            "website_url": "http://localhost:8000/",
            "amount": float(order.total_amount * 100),  # Correct Paisa conversion
            "purchase_order_id": unique_txn_id,        # Send your unique ID
            "purchase_order_name": f"Order #{order.id}",
        }

        response = requests.post(initiate_url, headers=headers, data=json.dumps(payload_dict))
        
        if response.status_code == 200:
            response_data = response.json()
            checkout_url = response_data.get("payment_url")
            khalti_pidx = response_data.get("pidx")

            # 3. Save/Update Payment Record
            payment_details, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'payment_method': 'khalti',
                    'amount': order.total_amount,
                    'status': 'pending', # Use 'initiated' as they are leaving your site
                    'transaction_id': unique_txn_id,
                    'payment_id': khalti_pidx,
                }
            )

            if not created:
                payment_details.payment_method = "khalti"
                payment_details.amount = order.total_amount
                payment_details.status = "pending"
                payment_details.transaction_id = unique_txn_id
                payment_details.payment_id = khalti_pidx
                payment_details.save()

            return redirect(checkout_url)

    def initiate_esewa_payment(self, request, order):
        ESEWA_MERCHANT_ID = settings.ESEWA_MERCHANT_ID
        ESEWA_SECRET_KEY = settings.ESEWA_SECRET_KEY

        unique_txn_id = f"ESEWA{order.id}_{int(time.time())}"
        
        amount_str = str(order.total_amount)

        input_text = f"total_amount={amount_str},transaction_uuid={unique_txn_id},product_code={ESEWA_MERCHANT_ID}"

        # HMAC SHA256 Logic
        hmac_sha256 = hmac.new(
            ESEWA_SECRET_KEY.encode('utf-8'), 
            input_text.encode('utf-8'), 
            hashlib.sha256
        )
        digest = hmac_sha256.digest()
        signature = base64.b64encode(digest).decode('utf-8')

        # Update or Create payment record
        payment_details, created = Payment.objects.update_or_create(
            order=order,
            defaults={
                'payment_method': 'esewa',
                'amount': order.total_amount,
                'status': 'pending',
                'transaction_id': unique_txn_id,
                'payment_id': unique_txn_id, # Usually updated after success
            }
        )

        if not created:
            payment_details.payment_method = "esewa"
            payment_details.amount = order.total_amount
            payment_details.status = "pending"
            payment_details.transaction_id = unique_txn_id
            payment_details.payment_id = unique_txn_id
            payment_details.save()

        context = {
            "esewa_data": {
                "amount": order.total_amount, 
                "transaction_uuid": unique_txn_id,
                "product_code": ESEWA_MERCHANT_ID, 
                "signature": signature,
            }
        }

        return render(request, 'customer_panel/esewa_confirmation.html', context)

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
            return render(request, 'customer_panel/checkout.html', context)
            
        except OrderCart.DoesNotExist:
            messages.error(request, "Order cart not found!")
            return redirect('order_cart')

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
                order_status='pending'
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
                return self.process_cod(request, order)
            elif payment_method == 'esewa':
                return self.initiate_esewa_payment(request, order)
            elif payment_method == 'khalti':
                return self.initiate_khalti_payment(request, order)
        
        except OrderCart.DoesNotExist:
            messages.error(request, "Order cart not found!")
            return redirect('order_cart')
        except ShippingAddress.DoesNotExist:
            messages.error(request, "Invalid shipping address!")
            return redirect('order_cart')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('order_cart')
            
