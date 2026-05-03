from django.urls import reverse
from django.views import generic
from payments.models import Payment
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin

from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin


class PaymentListView(AdminLoginRequiredMixin,generic.ListView):
    model = Payment
    template_name = 'admin_panel/admin_all_payments.html'
    context_object_name = 'payments'
    paginate_by = 10 

    def get_queryset(self):
        queryset = Payment.objects.all().order_by("-created_at")

        search_query = self.request.GET.get('search')
        status_filters = self.request.GET.getlist('status')

        if search_query:
            queryset = queryset.filter(
                Q(order__order_id__icontains=search_query) | 
                Q(transaction_id__icontains=search_query) |
                Q(payment_id__icontains=search_query)
    )
            return queryset

        if status_filters:
            queryset = queryset.filter(status__in=status_filters)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
            
        context['query_params'] = query_params.urlencode()
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filters'] = self.request.GET.getlist('status')
        context['payment_status_choices'] = Payment.PAYMENT_STATUS
        return context
    

class AdminPaymentEditView(AdminLoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Payment
    template_name = 'admin_panel/admin_payment_edit.html'
    fields = ['payment_method', 'status', 'transaction_id', 'payment_id', 'amount']
    context_object_name = 'payment'
    success_message = "Payment status updated successfully."

    def get_success_url(self):
        return reverse('admin_payments')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_status_choices'] = Payment.PAYMENT_STATUS
        return context