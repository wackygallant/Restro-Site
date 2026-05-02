from django import forms

class EmailVerificationForm(forms.Form):
    email = forms.EmailField()

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
