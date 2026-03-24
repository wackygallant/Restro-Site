# Django Modules Imports
from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Forms Import
from customer_panel.formsets.bookingform import BookingForm

# App Imports
from booking.models import Booking

# Custom Util Imports
from utils._utils import get_username

@method_decorator(login_required, name='dispatch')
class AllBookingsView(generic.TemplateView):
    template_name="customer_panel/all_bookings.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["bookings"] = Booking.objects.filter(user=self.request.user).order_by("-date")
        return context

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
            
            return render(request, "customer_panel/booktable.html", {
                "form": BookingForm(), # Reset with a fresh form    
                "message": "Booking confirmed successfully!",
                "username": get_username(request),
            })
        
        else:
            print("Form errors:", form.errors)
            
            return render(request, "customer_panel/booktable.html", {
                "form": form,
                "username": get_username(request)
            })
