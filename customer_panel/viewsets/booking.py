# Django Modules Imports
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View, generic
from django.contrib import messages

# Forms Import
from customer_panel.formsets.bookingform import BookingForm

# App Imports
from booking.models import Booking, TimeSlot

# Custom Util Imports
from utils._utils import get_username

class AllBookingsView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name="customer_panel/all_bookings.html"
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class BookTableView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "username": get_username(request),
            "time_slots": TimeSlot.objects.all().order_by('time'),
        }
        return render(request, "customer_panel/booktable.html", context)

    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            validate_date = form.cleaned_data['booking_date']
            
            if validate_date < timezone.now().date():
                messages.error(request, "Table booking failed. Cannot book a past date!")
                return redirect('booking_page')
            
            # If valid, proceed to save
            booking = form.save(commit=False)
            booking.user = request.user
            booking.booking_id = booking.create_booking_id()
            booking.save()
            
            messages.success(request, "Table booked successfully! Please wait for confirmation.")
            return redirect('booking_page')
    
        else:
            # Form-level validation errors (e.g. wrong format)
            return render(request, "customer_panel/booktable.html", {'form': form})
