from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import IntegrityError

from menu.models import MenuItems, MenuCategories
from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin
from admin_panel.formsets.menuitemform import MenuItemForm

# --- CATEGORY VIEWS ---

class AdminCategoryListView(AdminLoginRequiredMixin, generic.ListView):
    model = MenuCategories
    template_name = 'admin_panel/admin_all_categories.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = MenuCategories.objects.only('name', 'priority').order_by('priority')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

class AdminCategoryCreateView(AdminLoginRequiredMixin, generic.CreateView):
    model = MenuCategories
    template_name = 'admin_panel/admin_category_create.html'
    fields = ['name', 'priority']
    success_url = reverse_lazy('admin_categories')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class AdminCategoryEditView(AdminLoginRequiredMixin, generic.UpdateView):
    model = MenuCategories
    template_name = 'admin_panel/admin_category_edit.html'
    fields = ['name', 'priority']
    success_url = reverse_lazy('admin_categories')
    context_object_name = 'category'

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

class AdminCategoryDeleteView(AdminLoginRequiredMixin, generic.DeleteView):
    model = MenuCategories
    success_url = reverse_lazy('admin_categories')
    
    def get(self, request, *args, **kwargs):
        messages.success(self.request, 'Category deleted successfully!')
        return self.delete(request, *args, **kwargs)


# --- MENU ITEM VIEWS ---

class AdminMenuListView(AdminLoginRequiredMixin, generic.ListView):
    model = MenuItems
    template_name = 'admin_panel/admin_all_menu.html'
    context_object_name = 'menu_items'
    paginate_by = 10

    def get_queryset(self):
        queryset = MenuItems.objects.select_related('category').order_by('priority')
        
        search = self.request.GET.get('search')
        category_filters = self.request.GET.getlist('category')
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        if category_filters:
            queryset = queryset.filter(category_id__in=category_filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = MenuCategories.objects.only('id', 'name', 'priority').order_by('priority')
        return context

class AdminMenuCreateView(AdminLoginRequiredMixin, generic.CreateView):
    model = MenuItems
    form_class = MenuItemForm
    template_name = 'admin_panel/admin_menuitem_create.html'
    success_url = reverse_lazy('admin_menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MenuCategories.objects.only('id', 'name').order_by('priority')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Menu item created successfully!')
        return super().form_valid(form)

class AdminMenuEditView(AdminLoginRequiredMixin, generic.UpdateView):
    model = MenuItems
    form_class = MenuItemForm
    template_name = 'admin_panel/admin_menuitem_edit.html'
    success_url = reverse_lazy('admin_menu')
    context_object_name = 'menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MenuCategories.objects.only('id', 'name').order_by('priority')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Menu item updated successfully!')
        return super().form_valid(form)

class AdminMenuDeleteView(AdminLoginRequiredMixin, generic.DeleteView):
    model = MenuItems
    success_url = reverse_lazy('admin_menu')

    def get(self, request, *args, **kwargs):
        messages.success(self.request, 'Menu item deleted successfully!')
        return self.delete(request, *args, **kwargs)