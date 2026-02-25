from django import forms
from django.contrib.auth.models import User
from .models import Payment


class CheckoutForm(forms.Form):
    """Form for checkout process"""
    shipping_address = forms.IntegerField(
        widget=forms.RadioSelect,
        required=True,
        error_messages={'required': 'Please select a shipping address'}
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('cash_on_delivery', 'Cash on Delivery'),
            ('esewa', 'eSewa'),
            ('khalti', 'Khalti'),
        ],
        widget=forms.RadioSelect,
        required=True,
        error_messages={'required': 'Please select a payment method'}
    )


class PaymentVerificationForm(forms.Form):
    """Form for payment verification"""
    pidx = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.HiddenInput()
    )
    
    def clean_pidx(self):
        pidx = self.cleaned_data.get('pidx')
        if not pidx:
            raise forms.ValidationError('Payment ID is required')
        return pidx


class KhaltiPaymentForm(forms.ModelForm):
    """Form for Khalti payment processing"""
    
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount']
        widgets = {
            'payment_method': forms.HiddenInput(),
            'amount': forms.HiddenInput(),
        }
