from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from user_accounts.forms import SignUpForm, ShippingAddressForm
from booking.models import Booking
from order.models import Order
from user_accounts.models import ShippingAddress
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html',{})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials'})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
class RegisterView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'register.html', {'form' : form })
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Login the user after registration
            user = authenticate(username=username, password=password)
            login(request, user)
            message = 'Account created successfully'
            return redirect('home')
        else:
            message = 'Please correct the error below.'
        return render(request, 'register.html', {'form': form, 'message': message})
    
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        
        user = request.user
        bookings = Booking.objects.filter(user=user.username).order_by('-id')[:3]
        orders = Order.objects.filter(user=user.id).order_by('-id')[:3]
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
        return render(request, 'user_profile.html', context)

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
