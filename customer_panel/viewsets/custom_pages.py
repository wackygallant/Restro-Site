# Django Modules Imports
from django.shortcuts import render
from django.views import generic

# App Imports
from customer_panel.models import Teams, Reviews
from menu.models import MenuItems

# Custom Util Imports
from utils import _utils

class HomePage(generic.TemplateView):
    template_name = "customer_panel/index.html"

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context.update({
            "username": _utils.get_username(self.request),
            "reviews": Reviews.objects.all().order_by('-created_at')[:3],
            "menu_items": MenuItems.objects.all(),
            "special_items": MenuItems.objects.filter(is_on_special=True)
        })
        return context
    
class AboutPage(generic.TemplateView):
    template_name = "customer_panel/about.html"

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            "username": _utils.get_username(self.request),
            "teams": Teams.objects.all()
        })
        return context