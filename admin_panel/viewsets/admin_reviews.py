from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from customer_panel.models import Reviews
from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin
from django.contrib import messages


class AdminReviewsView(AdminLoginRequiredMixin, generic.ListView):
    template_name = 'admin_panel/admin_all_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Reviews.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(first_name__icontains=search) | queryset.filter(last_name__icontains=search) | queryset.filter(review__icontains=search)
        return queryset


class AdminReviewCreateView(AdminLoginRequiredMixin, generic.CreateView):
    model = Reviews
    template_name = 'admin_panel/admin_review_create.html'
    fields = ['first_name', 'last_name', 'review', 'rating']
    success_url = reverse_lazy('admin_reviews')
    success_message = "Review created successfully!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

class AdminReviewEditView(AdminLoginRequiredMixin, generic.UpdateView):
    model = Reviews
    template_name = 'admin_panel/admin_review_edit.html'
    fields = ['first_name', 'last_name', 'review', 'rating']
    success_url = reverse_lazy('admin_reviews')
    success_message = "Review updated successfully!"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.object
        return context

class AdminReviewDeleteView(AdminLoginRequiredMixin, generic.DeleteView):
    model = Reviews
    template_name = 'admin_panel/admin_review_delete.html'
    success_url = reverse_lazy('admin_reviews')
    success_message = "Review deleted successfully!"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, self.success_message)
        return redirect(success_url)
