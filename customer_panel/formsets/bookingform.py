from django import forms
from booking.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['email', 'phone_number', 'booking_date', 'time_slot', 'person_count']
