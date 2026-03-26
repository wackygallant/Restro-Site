# Django Modules Imports
from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

# Forms Import
from customer_panel.formsets.bookingform import BookingForm

# App Imports
from booking.models import Booking

# Custom Util Imports
from utils._utils import get_username

@method_decorator(login_required, name='dispatch')
class AllBookingsView(generic.ListView):
    model = Booking
    template_name="customer_panel/all_bookings.html"
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

@method_decorator(login_required, name='dispatch')
class BookTableView(View):
    def get(self, request):
        form = BookingForm()
        return render(request, "customer_panel/booktable.html", {
            "form": form,
            "username": get_username(request)
        })

    def post(self, request):
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            
            messages.success(request, "Booking confirmed successfully!")
            return render(request, "customer_panel/booktable.html", {
                "form": BookingForm(),
                "username": get_username(request),
            })
        
        else:
            messages.error(request, "Form errors: " + str(form.errors))
            
            return render(request, "customer_panel/booktable.html", {
                "form": form,
                "username": get_username(request)
            })
