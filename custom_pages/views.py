from django.shortcuts import render
from django.views import View
from custom_pages.models import Teams, Testimonials
from menu.models import MenuItems

from utils import _utils

class HomePage(View):
    def get(self, request):
        username = _utils.get_username(request)
        testimonials = Testimonials.objects.all()
        menu_items = MenuItems.objects.all()

        context = {
            "username": username,
            "testimonials" : testimonials,
            "menu_items": menu_items,
        }
        return render(request, "index.html", context)
    
class AboutPage(View):
    def get(self, request):
        username = _utils.get_username(request)
        teams = Teams.objects.all()
        context = {
            "teams": teams,
            "username": username,
        }
        return render(request, "about.html", context)