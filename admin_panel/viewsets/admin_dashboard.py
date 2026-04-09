# Django Modules Import
from django.views import View, generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum

# App Imports
from order.models import Order
from booking.models import Booking
from django.contrib.auth.models import User
from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin

class DashboardView(AdminLoginRequiredMixin, generic.TemplateView):
    template_name = 'admin_panel/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        completed_orders = Order.objects.filter(order_status='completed')
        confirmed_bookings = Booking.objects.filter(booking_status='confirmed')

        context.update({
            'total_users': User.objects.count(),
            'total_orders': completed_orders.count(),
            'total_revenue': completed_orders.aggregate(total=Sum('total_amount'))['total'] or 0,
            'total_reservations': confirmed_bookings.count(),
            'orders': Order.objects.all().order_by('-order_date')[:5]
        })
        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        request.session.flush()
        return redirect('login')

