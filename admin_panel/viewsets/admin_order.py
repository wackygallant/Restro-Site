# Django Module Imports
from django.views import generic, View
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
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
        queryset = Order.objects.select_related('user').prefetch_related('order_items').order_by("-order_date")

        search_query = self.request.GET.get('search')
        status_filters = self.request.GET.getlist('status')

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
        
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filters'] = self.request.GET.getlist('status')
        context['order_status_choices'] = Order.STATUS_CHOICES
        return context

# --- OPTIMIZED STATUS UPDATE VIEWS ---

class BaseOrderStatusUpdateView(AdminLoginRequiredMixin, View):
    """
    A base view to handle updating an order's status.
    This prevents us from writing the same code multiple times.
    """
    status_to_set = None
    success_message = ''

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        
        order.order_status = self.status_to_set
        order.save(update_fields=['order_status'])
        
        messages.success(request, self.success_message)
        return redirect('admin_orders')

class CompleteOrder(BaseOrderStatusUpdateView):
    status_to_set = 'completed'
    success_message = 'Order completed successfully!'

class CancelOrder(BaseOrderStatusUpdateView):
    status_to_set = 'cancelled'
    success_message = 'Order cancelled successfully!'