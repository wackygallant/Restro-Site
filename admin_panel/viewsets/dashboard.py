from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'admin_panel/dashboard.html'

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        request.session.flush()
        return redirect('login-user')

