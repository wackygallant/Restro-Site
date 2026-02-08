from django import forms
from django.utils import timezone 
# Better than standard datetime for Django
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['phone_number', 'email', 'date', 'time_slot', 'person_count']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '123-456-7890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'your@email.com'}),
            'person_count': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '2'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'time_slot': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }