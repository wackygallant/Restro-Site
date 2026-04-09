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
        users = User.objects.prefetch_related('bookings', 'orders').all()
        context.update({
            'total_users': users.count(),
            'total_orders': users.filter(orders__order_status='pending').count(),
            'total_revenue': users.filter(orders__order_status='completed').aggregate(total=Sum('orders__total_amount'))['total'] or 0,
            'total_reservations': users.filter(bookings__booking_status='confirmed').count(),
            'orders': users.filter(orders__order_status='pending').order_by('-orders__order_date')[:4],
        })
        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        request.session.flush()
        return redirect('login')

