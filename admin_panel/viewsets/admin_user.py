# Django Module Imports
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages

# App Imports
from django.contrib.auth.models import User
from ..formsets.usercreationform import AdminUserCreationForm

class UserAdminView(LoginRequiredMixin, generic.TemplateView):
    template_name="admin_panel/admin_all_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'users' : User.objects.all().order_by('date_joined'),
        })
        return context
class UserCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_panel/admin_user_create.html')

    def post(self, request):
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('admin_users')
        return render(request, 'admin_panel/admin_user_create.html', {'form': form})


# class UserEditView(LoginRequiredMixin, generic.TemplateView):
#     template_name="admin_panel/admin_user_edit.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context.update({
#             'user' : User.objects.get(pk=self.kwargs['pk']),
#         })
#         return context

# class UserDeleteView(LoginRequiredMixin, generic.View):
#     def get(self, request, pk):
#         user = User.objects.get(pk=pk)
#         user.delete()
#         return redirect('admin_user')

