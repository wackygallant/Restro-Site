from django import forms

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
