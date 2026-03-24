from django.shortcuts import render
from django.views import View, generic

from customer_panel.models import Teams, Testimonials
from menu.models import MenuItems

from utils import _utils

class HomePage(generic.TemplateView):
    template_name = "customer_panel/home.html"

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["username"] = _utils.get_username(self.request)
        context["testimonials"] = Testimonials.objects.all()
        context["menu_items"] = MenuItems.objects.all()
        return context
    
class AboutPage(View):
    template_name = "customer_panel/about.html"

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["username"] = _utils.get_username(self.request)
        context["teams"] = Teams.objects.all()
        return context