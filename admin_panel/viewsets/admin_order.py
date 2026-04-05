# Django Module Imports
from django.views import generic, View
from django.shortcuts import redirect
from django.contrib import messages

# App Imports
from order.models import Order

class AdminOrderView(generic.ListView):
    template_name = "admin_panel/admin_all_order.html"
    context_object_name = "orders"
    model = "Order"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.all().order_by("-order_date")

class AdminOrderItemsView(generic.TemplateView):
    template_name = "admin_panel/admin_order_items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)


        context.update({
            "order_items": order.order_items.all(),
            "order": order,
        })
        return context

class StatusUpdate(View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        order.order_status = 'completed'
        order.save()
        messages.success(request, 'Order status updated successfully!')
        return redirect('admin_orders')