from django.shortcuts import render
from django.views import View

class BookingPage(View):
    def get(self, request):
        return render(request, "booktable.html", {})
