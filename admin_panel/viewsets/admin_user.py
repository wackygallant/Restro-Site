# Django Module Imports
from django.views import generic, View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# App Imports
from django.contrib.auth.models import User
from admin_panel.formsets.usercreationform import Admin_UserCreationForm
from user_accounts.viewsets.CustomMixin import AdminLoginRequiredMixin
from admin_panel.formsets.usereditform import Admin_UserEditForm

class UserAdminView(AdminLoginRequiredMixin, generic.ListView):
    template_name="admin_panel/admin_all_user.html"
    context_object_name = 'users'
    model = User
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search')
        filters = self.request.GET.getlist('status')
        if search is not None or filters:
            queryset = User.objects.exclude(is_superuser=True)
            if search:
                queryset = queryset.filter(username__icontains=search)
            if filters:
                queryset = queryset.filter(is_active=True) if 'active' in filters else queryset
                queryset = queryset.filter(is_staff=True) if 'staff' in filters else queryset
            return queryset.order_by('-date_joined')
        return User.objects.exclude(is_superuser=True).order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filters'] = self.request.GET.getlist('status')
        return context

class UserCreateView(AdminLoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/admin_user_create.html')

    def post(self, request):
        form = Admin_UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully!')
            if request.POST.get('sendWelcomeEmail') == 'on':
                send_mail(f'Welcome {user.username}', f'Your Account with username {user.username} has been created successfully.\nThank you for joining us.', settings.DEFAULT_FROM_EMAIL, [user.email])
            return redirect('admin_users')
        return render(request, 'admin_panel/admin_user_create.html', {'form': form})

class UserEditView(AdminLoginRequiredMixin, View):
    template_name="admin_panel/admin_user_edit.html"

    def get(self, request, pk):
        context = {
            'edit_user': User.objects.get(pk=pk),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        edit_user = User.objects.get(pk=pk)
        form = Admin_UserEditForm(request.POST, instance=edit_user) 
        
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
        else:
            messages.error(request, f"Update failed: {form.errors.as_text()}")
            
        return redirect('admin_users')

class UserDeleteView(AdminLoginRequiredMixin, View):
    def get(self, request, pk):
        edit_user = User.objects.get(pk=pk)
        edit_user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('admin_users')

        password1, password2 = request.POST['password1'], request.POST['password2']
        if password1 != password2:
            context = {
            'edit_user' : User.objects.get(id=pk),
            }
            messages.error(request, f"Failed to Change Password for {editing_user.username}!")
            return render(request, 'authentication/change_password.html', context)
        
        editing_user = User.objects.get(id=pk)
        editing_user.set_password(request.POST['password1'])
        editing_user.save()
        messages.success(request, f"Password Changed for {editing_user.username} successfully!")
        return redirect("admin_users")