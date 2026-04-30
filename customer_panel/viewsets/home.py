# Django Modules Imports
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages

# App Imports
from customer_panel.models import Teams, Reviews
from menu.models import MenuItems
from admin_panel.formsets.reviewform import ReviewForm

# Custom Util Imports
from utils import _utils

class HomePage(generic.TemplateView):
    template_name = "customer_panel/index.html"

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context.update({
            "username": _utils.get_username(self.request),
            "reviews": Reviews.objects.all().order_by('-created_at')[:6],
            "menu_items": MenuItems.objects.all(),
            "special_items": MenuItems.objects.filter(is_on_special=True)
        })
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request ,"Review Updated Successfully")
            return redirect('home')
            
        messages.error(request, form.error)
        return redirect('home')

class AboutPage(generic.TemplateView):
    template_name = "customer_panel/about.html"

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({
            "username": _utils.get_username(self.request),
            "teams": Teams.objects.all()
        })
        return context