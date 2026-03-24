from django import forms
from user_accounts.models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['contact_no', 'address', 'city']