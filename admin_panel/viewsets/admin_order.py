# Django Module Imports
from django.views import generic, View
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages

# App Imports
from order.models import Order
from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin

class AdminOrderView(AdminLoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "admin_panel/admin_all_order.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        # 1. Base Queryset with optimizations
        queryset = Order.objects.select_related('user').prefetch_related('order_items').order_by("-order_date")

        # 2. Get parameters from request
        search_query = self.request.GET.get('search')
        status_filters = self.request.GET.getlist('status')

        # 3. Apply logic conditionally
        if search_query:
            queryset = queryset.filter(
                Q(order_id__icontains=search_query) | 
                Q(user__username__icontains=search_query)
            )

        if status_filters:
            queryset = queryset.filter(order_status__in=status_filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass filters back to the template to persist form state
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filters'] = self.request.GET.getlist('status')
        context['order_status_choices'] = Order.STATUS_CHOICES
        return context

class CompleteOrder(AdminLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        order.order_status = 'completed'
        order.save()
        messages.success(request, 'Order completed successfully!')
        return redirect('admin_orders')
        
class CancelOrder(AdminLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        order.order_status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
        return redirect('admin_orders')