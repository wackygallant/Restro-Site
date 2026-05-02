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
    template_name = "customer_panel/all_orders.html"
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
            order_cart_item.quantity += quantity
            order_cart_item.save()

        messages.success(request, f"{menu_item.name} added to order cart!")
        return redirect('orders')


class RemoveFromOrderCartView(LoginRequiredMixin, View):
    """Remove item from order cart"""
    def post(self, request, order_cart_item_id):
        order_cart_item = get_object_or_404(
            OrderCartItem, id=order_cart_item_id, order_cart__user=request.user
        )
        menu_item_name = order_cart_item.menu_item.name
        order_cart_item.delete()
        messages.success(request, f"{menu_item_name} removed from order cart!")
        return redirect('order_cart')


class UpdateOrderCartItemView(LoginRequiredMixin, View):
    """Update quantity of item in order cart"""
    def post(self, request, order_cart_item_id):
        quantity_str = request.POST.get('quantity', '1').strip()
        quantity = int(quantity_str) if quantity_str else 1
        order_cart_item = get_object_or_404(
            OrderCartItem, id=order_cart_item_id, order_cart__user=request.user
        )

        if quantity > 0:
            order_cart_item.quantity = quantity
            order_cart_item.save()
            messages.success(request, "Order cart updated!")
        else:
            order_cart_item.delete()
            messages.success(request, "Item removed from order cart!")

        return redirect('order_cart')


class PaymentVerificationView(LoginRequiredMixin, generic.TemplateView):
    template_name = "customer_panel/payment_verify.html"

    def handle_khalti_payment_verification(self, request):
        params = request.GET.dict()
        pidx = params.get("pidx", "")
        purchase_order_id = params.get("purchase_order_id", "")

        # Guard: find the payment record
        payment_details = Payment.objects.filter(transaction_id=purchase_order_id).first()
        if not payment_details:
            messages.error(request, "Payment record not found.")
            return redirect("orders")

        order = payment_details.order

        # Guard: prevent re-processing an already completed payment
        if payment_details.status == "paid":
            messages.info(request, "This payment has already been verified.")
            return redirect("orders")

        verify_url = f"{settings.KHALTI_API_URL}epayment/lookup/"
        headers = {
            "Authorization": f"Key {settings.KHALTI_API_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        # Hit Khalti verification API
        try:
            response = requests.post(
                verify_url, headers=headers,
                json={"pidx": pidx}, timeout=10
            )
            response_data = response.json()
        except requests.exceptions.Timeout:
            # Unknown outcome — keep order, mark failed, let admin investigate
            order.order_status = "failed"
            order.save()
            messages.error(request, "Khalti verification timed out. Please contact support.")
            return redirect("orders")
        except Exception:
            order.order_status = "failed"
            order.save()
            messages.error(request, "Could not connect to Khalti. Please contact support.")
            return redirect("orders")

        # SUCCESS PATH
        if response.status_code == 200 and response_data.get("status") == "Completed":
            with transaction.atomic():
                payment_details.status = "paid"
                payment_details.save()

                order.order_status = "completed"
                order.save()

                try:
                    cart = OrderCart.objects.get(user=request.user)
                    cart.order_cart_items.all().delete()
                except OrderCart.DoesNotExist:
                    pass
                except Exception as e:
                    print(f"Cart clearing error: {e}")

            messages.success(request, "Payment successful via Khalti!")
            return redirect("orders")

        # FAILURE PATH — be surgical about what we delete
        khalti_status = response_data.get("status", "")

        if khalti_status in ("Expired", "Canceled", "User canceled"):
            # Explicit cancellation/expiry — safe to clean up
            with transaction.atomic():
                payment_details.delete()
                order.delete()  # Cascades to OrderItems
            messages.error(request, f"Payment {khalti_status.lower()}. Your order has been removed.")
        else:
            # Ambiguous failure (Khalti 5xx, unknown status) — keep for admin review
            order.order_status = "failed"
            order.save()
            error_msg = response_data.get("detail", "Payment could not be verified.")
            messages.error(request, f"Khalti Error: {error_msg}. Please contact support.")

        return redirect("orders")

    def handle_esewa_payment_verification(self, request):
        params = request.GET.dict()
        data = params.get("data", "")

        try:
            json_data = json.loads(base64.b64decode(data))
        except Exception:
            messages.error(request, "Invalid eSewa response.")
            return redirect("orders")

        total_amount = json_data.get("total_amount")
        transaction_uuid = json_data.get("transaction_uuid")

        status_check_url = (
            f"https://rc.esewa.com.np/api/epay/transaction/status/"
            f"?product_code={settings.ESEWA_MERCHANT_ID}"
            f"&total_amount={total_amount}"
            f"&transaction_uuid={transaction_uuid}"
        )

        try:
            response = requests.get(status_check_url, timeout=10)
            response_data = response.json()
        except Exception:
            messages.error(request, "Could not verify eSewa payment.")
            return redirect("orders")

        if response.status_code == 200 and response_data.get('status') == "COMPLETE":
            pending = request.session.pop('pending_esewa_order', None)

            if not pending or pending['transaction_uuid'] != transaction_uuid:
                messages.error(request, "Session mismatch. Please contact support.")
                return redirect("orders")

            # Payment confirmed — create order, items, and payment record now
            with transaction.atomic():
                order = Order(
                    user=request.user,
                    shippingaddress=pending['shipping_address'],
                    order_status='completed',
                    total_amount=pending['total_amount'],
                )
                # FIX: generate the order_id before saving
                order.create_order_id()
                order.save()

                for item_data in pending['cart_snapshot']:
                    menu_item = MenuItems.objects.get(id=item_data['menu_item_id'])
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=item_data['quantity'],
                        price=item_data['price'],
                    )

                Payment.objects.create(
                    order=order,
                    payment_method='esewa',
                    amount=pending['total_amount'],
                    status='paid',
                    transaction_id=transaction_uuid,
                    payment_id=transaction_uuid,
                )

                try:
                    cart = OrderCart.objects.get(user=request.user)
                    cart.order_cart_items.all().delete()
                except OrderCart.DoesNotExist:
                    pass
                except Exception as e:
                    print(f"Cart clearing error: {e}")

            messages.success(request, "Payment successful via eSewa!")
            return redirect('orders')

        else:
            request.session.pop('pending_esewa_order', None)
            error_msg = response_data.get("detail", "Payment was not completed.")
            messages.error(request, f"eSewa Error: {error_msg}")
            return redirect("orders")

    def get(self, request, *args, **kwargs):
        """
        Route to the correct payment handler based on query params.
        NOTE: transaction.atomic() is intentionally NOT wrapping the entire
        routing block — each handler manages its own atomic sections internally.
        """
        params = request.GET.dict()
        purchase_order_id = params.get('purchase_order_id', '')

        try:
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
        """Order already saved — just create payment record and clear cart."""
        Payment.objects.create(
            order=order,
            payment_method='cash_on_delivery',
            amount=order.total_amount,
            status='pending'
        )
        try:
            cart = OrderCart.objects.get(user=request.user)
            cart.order_cart_items.all().delete()
        except Exception as e:
            print(f"Error clearing order cart: {e}")

        messages.success(request, "Order placed successfully! Pay on delivery.")
        return redirect('orders')

    def initiate_khalti_payment(self, request, order):
        """
        Order is already saved when this is called (needed for the order ID).
        Hits Khalti API — deletes the order if initiation fails.
        """
        url = settings.KHALTI_API_URL
        secret_key = settings.KHALTI_API_SECRET_KEY

        if not url or not secret_key:
            order.delete()
            messages.error(request, "Khalti is not configured.")
            return redirect('checkout')

        unique_txn_id = f"KHALTI_{order.id}_{int(time.time())}"
        initiate_url = f"{url}epayment/initiate/"

        headers = {
            'Authorization': f'Key {secret_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            "return_url": "http://localhost:8000/payment_verify/",
            "website_url": "http://localhost:8000/",
            "amount": float(order.total_amount * 100),
            "purchase_order_id": unique_txn_id,
            "purchase_order_name": f"Order #{order.order_id}",
        }

        try:
            response = requests.post(
                initiate_url, headers=headers,
                json=payload, timeout=10
            )
        except requests.exceptions.RequestException:
            order.delete()  # Cascades to OrderItems
            messages.error(request, "Could not connect to Khalti. Please try again.")
            return redirect('checkout')

        if response.status_code == 200:
            response_data = response.json()
            checkout_url = response_data.get("payment_url")
            khalti_pidx = response_data.get("pidx")

            if not checkout_url or not khalti_pidx:
                order.delete()
                messages.error(request, "Invalid response from Khalti.")
                return redirect('checkout')

            # Khalti confirmed — create payment record and redirect
            Payment.objects.create(
                order=order,
                payment_method='khalti',
                amount=order.total_amount,
                status='pending',
                transaction_id=unique_txn_id,
                payment_id=khalti_pidx,
            )
            return redirect(checkout_url)

        else:
            order.delete()
            try:
                error_detail = response.json().get("detail", "Khalti initiation failed.")
            except Exception:
                error_detail = "Khalti initiation failed."
            messages.error(request, f"Khalti Error: {error_detail}")
            return redirect('checkout')

    def initiate_esewa_payment(self, request, order, order_cart_items):
        """
        Does NOT persist the order. Stores order intent in the session.
        The real order is created only after eSewa verification succeeds.
        """
        ESEWA_MERCHANT_ID = settings.ESEWA_MERCHANT_ID
        ESEWA_SECRET_KEY = settings.ESEWA_SECRET_KEY

        unique_txn_id = f"ESEWA{order.id}_{int(time.time())}"
        amount_str = str(order.total_amount)

        input_text = (
            f"total_amount={amount_str},"
            f"transaction_uuid={unique_txn_id},"
            f"product_code={ESEWA_MERCHANT_ID}"
        )
        hmac_sha256 = hmac.new(
            ESEWA_SECRET_KEY.encode('utf-8'),
            input_text.encode('utf-8'),
            hashlib.sha256
        )
        signature = base64.b64encode(hmac_sha256.digest()).decode('utf-8')

        # Snapshot cart items for order reconstruction on verification
        cart_snapshot = [
            {
                "menu_item_id": item.menu_item.id,
                "quantity": item.quantity,
                "price": str(
                    item.menu_item.special_price
                    if item.menu_item.is_on_special and item.menu_item.special_price
                    else item.menu_item.price
                ),
            }
            for item in order_cart_items
        ]

        # Store pending order intent in session — no DB write
        request.session['pending_esewa_order'] = {
            'shipping_address': order.shippingaddress,
            'total_amount': amount_str,
            'transaction_uuid': unique_txn_id,
            'cart_snapshot': cart_snapshot,
        }

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
        """Process checkout — create order in DB, then route to payment method."""
        checkout_form = CheckoutForm(request.POST)

        if not checkout_form.is_valid():
            messages.error(request, "Please correct the errors below")
            return self.get(request)

        try:
            order_cart = OrderCart.objects.get(user=request.user)
            order_cart_items = order_cart.order_cart_items.select_related('menu_item').all()

            if not order_cart_items.exists():
                messages.error(request, "Your order cart is empty!")
                return redirect('order_cart')

            shipping_address_id = checkout_form.cleaned_data['shipping_address']
            payment_method = checkout_form.cleaned_data['payment_method']

            shipping_address_obj = get_object_or_404(
                ShippingAddress, id=shipping_address_id, username=request.user
            )
            shipping_address = f"{shipping_address_obj.address}, {shipping_address_obj.city}"

            # Build and save order — needed to get a PK for all payment methods.
            # eSewa will delete it before returning; Khalti deletes it on failure.
            with transaction.atomic():
                order = Order(
                    user=request.user,
                    shippingaddress=shipping_address,
                    order_status='pending',
                )
                order.create_order_id()
                order.save()

                for item in order_cart_items:
                    OrderItem.objects.create(
                        order=order,
                        menu_item=item.menu_item,
                        quantity=item.quantity,
                        price=(
                            item.menu_item.special_price
                            if item.menu_item.is_on_special and item.menu_item.special_price
                            else item.menu_item.price
                        )
                    )
                order.calculate_total()

            if payment_method == 'cash_on_delivery':
                return self.process_cod(request, order)

            elif payment_method == 'esewa':
                # Build session snapshot then immediately clean up the temp order
                result = self.initiate_esewa_payment(request, order, order_cart_items)
                order.delete()  # Cascades to OrderItems; real order created on verification
                return result

            elif payment_method == 'khalti':
                # Handler deletes order internally on failure
                return self.initiate_khalti_payment(request, order)

            else:
                order.delete()
                messages.error(request, "Invalid payment method selected.")
                return redirect('checkout')

        except OrderCart.DoesNotExist:
            messages.error(request, "Order cart not found!")
            return redirect('order_cart')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('order_cart')