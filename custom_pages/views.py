from django.shortcuts import render
from django.views import View

class HomePage(View):
    def get(self, request):
        return render(request, "index.html", {})
    
class AboutPage(View):
    def get(self, request):
        return render(request, "about.html", {})