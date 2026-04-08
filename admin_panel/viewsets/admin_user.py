# Django Module Imports
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# App Imports
from django.contrib.auth.models import User
from ..formsets.usercreationform import Admin_UserCreationForm

class UserAdminView(LoginRequiredMixin, generic.ListView):
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
            return queryset.order_by('date_joined')
        return User.objects.exclude(is_superuser=True).order_by('date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filters'] = self.request.GET.getlist('status')
        return context


class UserCreateView(LoginRequiredMixin, View):
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


class UserEditView(LoginRequiredMixin, View):
    template_name="admin_panel/admin_user_edit.html"

    def get(self, request, pk):
        context = {
            'user': User.objects.get(pk=pk),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.is_superuser = True if request.POST.get('is_superuser') == 'on' else False
        user.is_staff = True if request.POST.get('is_staff') == 'on' else False
        user.is_active = True if request.POST.get('is_active') == 'on' else False
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('admin_users')

class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('admin_users')

