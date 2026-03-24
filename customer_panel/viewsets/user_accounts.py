# Django Modules Imports
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

# Form Imports
from customer_panel.formsets.shippingaddform import ShippingAddressForm

# App Imports
from booking.models import Booking
from order.models import Order
from user_accounts.models import ShippingAddress
    
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        user = request.user
        bookings = Booking.objects.filter(user=user.username).order_by('-date')[:3]
        orders = Order.objects.filter(user=user.id).order_by('-order_date')[:3]
        shipping_addresses = ShippingAddress.objects.filter(username=user)

        
        context = {
            'user': user,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined,
            'bookings': bookings,
            'orders' : orders,
            'shipping_addresses': shipping_addresses,
        }
        return render(request, 'customer_panel/user_profile.html', context)

class AddShippingAddressView(View):
    def post(self, request):
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.username = request.user
            address.save()
            messages.success(request, 'Address added successfully')
        else:
            messages.error(request, 'Please correct the errors below')
        return redirect('profile')

class EditShippingAddressView(View):
    def get(self, request, pk):
        address = ShippingAddress.objects.get(id=pk, username=request.user)
        form = ShippingAddressForm(instance=address)
        return render(request, 'edit_shipping_address.html', {'form': form, 'address': address})
    
    def post(self, request, pk):
        address = ShippingAddress.objects.get(id=pk, username=request.user)
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully')
        else:
            messages.error(request, 'Please correct the errors below')
        return redirect('profile')

class DeleteShippingAddressView(View):
    def post(self, request):
        address_id = request.POST.get('address_id')
        if address_id:
            try:
                address = ShippingAddress.objects.get(id=address_id, username=request.user)
                address.delete()
                messages.success(request, 'Address deleted successfully')
            except ShippingAddress.DoesNotExist:
                messages.error(request, 'Address not found')
        return redirect('profile')
