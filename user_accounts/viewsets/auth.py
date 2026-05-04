# Django Modules Imports
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from user_accounts.formsets.resetpassform import EmailVerificationForm, OTPVerificationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

# Form Imports
from user_accounts.formsets.user_register_form import SignUpForm
from user_accounts.models import OTP

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
            match user.is_staff:
                case True:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('admin_dashboard')
                case False:
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
        request.session.flush()
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
            
            # Sending Welcome Email to the User
            recipient = form.cleaned_data.get('email')
            send_mail("Welcome Email", f"Welcome {form.cleaned_data.get('first_name')}! for being a part of our Restro. \n Enjoy your best dining experience with us", settings.DEFAULT_FROM_EMAIL, [recipient])
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})

class ForgotPasswordView(View):

    template_name = 'authentication/forgot_password.html'

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
                    return redirect('login')
                else:
                    messages.error(request, "Invalid or expired OTP.")
            
            return render(request, self.template_name, {'form': form, 'email': email, 'step': 2})    

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

class ChangePasswordView(View):

    def get(self, request, pk):
        editing_user = User.objects.get(id=pk)
        return render(request, 'authentication/change_password.html', {'edit_user': editing_user})

    def post(self, request, pk):
        editing_user = User.objects.get(id=pk)
        
        is_admin = request.user.is_superuser
        current_pwd = request.POST.get('password') # The "Old/Admin" password for verification
        
        if not is_admin:
            if not current_pwd or not check_password(current_pwd, request.user.password):
                messages.error(request, "Incorrect current password.")
                return self.get(request, pk)

        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')

        if p1 != p2:
            messages.error(request, "New passwords do not match!")
            return self.get(request, pk)

        try:
            validate_password(p1, user=editing_user)
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
            return self.get(request, pk)

        editing_user.set_password(p1)
        editing_user.save()
        
        messages.success(request, f"Password for {editing_user.username} updated!")
        return redirect("admin_users")