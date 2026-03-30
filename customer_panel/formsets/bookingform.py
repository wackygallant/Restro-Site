from django import forms
from django.utils import timezone
from booking.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['phone_number', 'booking_date', 'time_slot', 'person_count']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'example@email.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '123-456-7890'}),
            'person_count': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '2'}),
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'time_slot': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }