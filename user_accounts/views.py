from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from user_accounts.forms import SignUpForm
from booking.models import Booking
from order.models import Order, OrderItem

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
        bookings = Booking.objects.filter(user=user.username).order_by('-date')
        orders = Order.objects.all()
        order_items = OrderItem.objects.filter()
        
        context = {
            'user': user,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined,
            'bookings': bookings,
            'orders' : orders,
            'order_items' : order_items,
        }
        return render(request, 'user_profile.html', context)