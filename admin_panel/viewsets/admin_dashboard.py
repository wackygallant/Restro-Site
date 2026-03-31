# Django Modules Import
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum, Count

# Model Imports
from order.models import Order
from booking.models import Booking
from django.contrib.auth.models import User

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'admin_panel/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_users': User.objects.filter(is_superuser=False).count(),
            'total_orders': Order.objects.count(),
            'total_revenue': Order.objects.filter(order_status='completed').aggregate(total=Sum('total_amount'))['total'] or 0,
            'total_reservations': Booking.objects.count(),
            'orders': Order.objects.all().order_by('-order_date')[:4],
        })
        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        request.session.flush()
        return redirect('login')

