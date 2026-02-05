from django.shortcuts import render
from django.views import View

from utils import _utils

class BookingPage(View):
    def get(self, request):
        username = _utils.get_username(request)
        return render(request, "booktable.html", {'username': username})
