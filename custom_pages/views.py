from urllib import request
from django.shortcuts import render
from django.views import View

from utils import _utils

class HomePage(View):
    def get(self, request):
        username = _utils.get_username(request)
        return render(request, "index.html", {"username": username})
    
class AboutPage(View):
    def get(self, request):
        username = _utils.get_username(request)
        return render(request, "about.html", {"username": username})