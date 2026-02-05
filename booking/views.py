from django.shortcuts import redirect, render
from django.views import View

from .models import Booking, TimeSlot

from utils import _utils

from datetime import datetime

class BookingPage(View):
    def get(self, request):
        username = _utils.get_username(request)
        time_slots = TimeSlot.objects.all().order_by('time')
        return render(request, "booktable.html", {'username': username, 'time_slots': time_slots})

    def post(self, request):
        # Handle booking form submission
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        person_count = request.POST.get('person_count')
        date = request.POST.get('date')
        # Format to HH:MM
        time_str = request.POST.get('time_slot')
        time_str = time_str.replace("a.m.", "AM").replace("p.m.", "PM").upper()
        t = datetime.strptime(time_str, "%I %p")
        time_slot = t.strftime("%H:%M")
        
        # Create a new booking instance
        Booking.objects.create(
            user=username,
            phone_number=phone_number,
            email=email,
            date=date,
            time_slot=TimeSlot.objects.get(time=time_slot),
            person_count=person_count
        )
        # Process booking data here (not implemented)
        return redirect('booking_page')
