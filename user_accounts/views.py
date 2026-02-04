from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    def get(self, request):
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
        return redirect('login')
    
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', {})