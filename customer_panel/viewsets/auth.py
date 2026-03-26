# Django Modules Imports
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from customer_panel.formsets.resetpassform import EmailVerificationForm, OTPVerificationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

# Form Imports
from customer_panel.formsets.registerform import SignUpForm
from user_accounts.models import OTP
from django.contrib.auth import get_user_model

# Custom Utils Imports
from utils._utils import generate_otp


User = get_user_model()

class LoginView(View):
    template_name = 'authentication/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name,{})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, self.template_name, {})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged Out Successfully!')
        return redirect('home')
    
class RegisterView(View):
    template_name = 'authentication/register.html'
    
    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form' : form })
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Login the user after registration
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully') 
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})

class PasswordResetView(View):
    template_name = 'authentication/reset-password.html'

    def get(self, request):
        # Initial state: Show the email entry form
        form = EmailVerificationForm()
        return render(request, self.template_name, {'form': form, 'step': 1})

    def post(self, request):
        # Determine which step we are on based on a hidden input in the HTML
        step = int(request.POST.get('step', 1))
        email = request.POST.get('email')

        if step == 1:
            form = EmailVerificationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if User.objects.filter(email=email).exists():
                    # Check if active OTP exists to prevent spam
                    active_otp = OTP.objects.filter(email=email).first()
                    if active_otp and active_otp.is_active():
                        messages.info(request, "OTP already sent. Please check your inbox.")
                    else:
                        otp = generate_otp()
                        send_mail('Reset OTP', f'Your OTP: {otp}', settings.DEFAULT_FROM_EMAIL, [email])
                        OTP.objects.update_or_create(email=email, defaults={'otp': otp})
                    
                    # Move to Step 2
                    new_form = OTPVerificationForm()
                    return render(request, self.template_name, {'form': new_form, 'email': email, 'step': 2})
                else:
                    messages.error(request, "Email not found.")
            return render(request, self.template_name, {'form': form, 'step': 1})

        elif step == 2:
            form = OTPVerificationForm(request.POST)
            if form.is_valid():
        
                otp_code = form.cleaned_data.get('otp')
                password = form.cleaned_data.get('new_password')
                confirm_p = form.cleaned_data.get('confirm_password')
        

                if password != confirm_p:
                    messages.error(request, "Passwords do not match.")
                    return render(request, self.template_name, {'form': form, 'email': email, 'step': 2})

                otp_record = OTP.objects.filter(email=email, otp=otp_code).first()
                if otp_record and otp_record.is_active():
                    user = User.objects.get(email=email)
            
                    user.set_password(password)
                    user.save()
                    OTP.objects.filter(email=email).delete()
                    messages.success(request, "Password reset successful!")
                    return redirect('login-user')
                else:
                    messages.error(request, "Invalid or expired OTP.")
            
            return render(request, self.template_name, {'form': form, 'email': email, 'step': 2})