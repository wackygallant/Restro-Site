from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from booking.forms import BookingForm

from booking.models import Booking
from utils._utils import get_username

@method_decorator(login_required, name='dispatch')
class BookTableView(View):#
    def get(self, request):
        form = BookingForm()
        return render(request, "booktable.html", {
            "form": form,
            "username": get_username(request)
        })

    def post(self, request):
        form = BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            
            return render(request, "booktable.html", {
                "form": BookingForm(), # Reset with a fresh form    
                "message": "Booking confirmed successfully!",
                "username": get_username(request),
            })
        
        else:
            print("Form errors:", form.errors)
            
            return render(request, "booktable.html", {
                "form": form,
                "username": get_username(request)
            })

@method_decorator(login_required, name='dispatch')
class AllBookingsView(generic.TemplateView):
    template_name="all_bookings.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["bookings"] = Booking.objects.order_by("-date")
        return context