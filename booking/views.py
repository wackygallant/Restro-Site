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
        date = request.POST.get('date')
        # Format to HH:MM
        time_str = request.POST.get('time_slot')
        time_str = time_str.replace("a.m.", "AM").replace("p.m.", "PM").upper()
        t = datetime.strptime(time_str, "%I %p")
        time_slot = t.strftime("%H:%M")
        
        table_count = request.POST.get('table_count')
        
        breakpoint()
        # Create a new booking instance
        Booking.objects.create(
            user=username,
            date=date,
            time_slot=TimeSlot.objects.get(time=time_slot),
            table_count=table_count
        )
        # Process booking data here (not implemented)
        return redirect('booking_page')