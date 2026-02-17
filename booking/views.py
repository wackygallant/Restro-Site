from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from booking.forms import BookingForm

from utils._utils import get_username

@method_decorator(login_required, name='dispatch')
class BookTableView(View):
    def get(self, request):
        form = BookingForm()
        return render(request, "booktable.html", {
            "form": form,
            "username": get_username(request)
        })

    def post(self, request):
        form = BookingForm(request.POST)
        
        # 1. Check validity FIRST
        if form.is_valid():
            # 2. Create the object but don't hit the database yet (commit=False)
            booking = form.save(commit=False)
            
            # 3. Manually set the user to the authenticated user
            booking.user = request.user
            
            # 4. Now save to the database
            booking.save()
            
            return render(request, "booktable.html", {
                "form": BookingForm(), # Reset with a fresh form    
                "message": "Booking confirmed successfully!",
                "username": get_username(request),
            })
        
        else:
            # If form is invalid, Django automatically populates form.errors
            print("Form errors:", form.errors)
            
            return render(request, "booktable.html", {
                "form": form, # Send the form back with error messages
                "username": get_username(request)
            })