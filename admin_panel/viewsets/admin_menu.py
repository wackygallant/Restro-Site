# Django Module Imports
from weakref import ref
from django.views import generic
from django.shortcuts import redirect

# App Imports
from menu.models import MenuItems, MenuCategories
from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy

class AdminCategoryListView(AdminLoginRequiredMixin, generic.ListView):
    model = MenuCategories
    template_name = 'admin_panel/admin_all_categories.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('priority')


class AdminCategoryCreateView(generic.CreateView):
    model = MenuCategories
    template_name = 'admin_panel/admin_category_create.html'
    context_object_name = 'category'
    fields = ['name', 'priority']
    success_message = 'Category created successfully!'
    success_url = reverse_lazy('admin_categories')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            # Handle cases where the DB rejects the save
            form.add_error(None, "A category with this specific attribute already exists.")
            return self.form_invalid(form)
        except Exception as e:
            # Handle unexpected errors
            form.add_error(None, f"An unexpected error occurred: {e}")
            return self.form_invalid(form)

class AdminCategoryEditView(AdminLoginRequiredMixin, generic.DetailView):
    model = MenuCategories
    template_name = 'admin_panel/admin_category_edit.html'
    context_object_name = 'category'

    def post(self, request, *args, **kwargs):
        try:    
            category = self.get_object()
            category.name = request.POST.get('name')
            category.priority = request.POST.get('priority')
            category.save()
            messages.success(request, 'Category updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating category: {str(e)}')
        return redirect(reverse_lazy('admin_categories'))

class AdminCategoryDeleteView(AdminLoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            category = MenuCategories.objects.get(pk=pk)
            category.delete()
            messages.success(request, 'Category deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting category: {str(e)}')
        return redirect(reverse_lazy('admin_categories'))

class AdminMenuListView(AdminLoginRequiredMixin, generic.ListView):
    model = MenuItems
    template_name = 'admin_panel/admin_all_menu.html'
    context_object_name = 'menu_items'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset.order_by('priority')
