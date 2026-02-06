from urllib import request
from django.shortcuts import render
from django.views import View
from custom_pages.models import Chefs, Testimonials

from utils import _utils

class HomePage(View):
    def get(self, request):
        username = _utils.get_username(request)
        testimonials = Testimonials.objects.all()
        context = {
            "username": username,
            "testimonials" : testimonials
        }
        return render(request, "index.html", context)
    
class AboutPage(View):
    def get(self, request):
        username = _utils.get_username(request)
        chefs = Chefs.objects.all()
        context = {
            "chefs": chefs,
            "username": username,
        }
        return render(request, "about.html", context)