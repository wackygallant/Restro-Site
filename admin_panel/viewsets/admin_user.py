# Django Module Imports
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# App Imports
from django.contrib.auth.models import User

class UserAdminView(LoginRequiredMixin, generic.TemplateView):
    template_name="admin_panel/admin_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'users' : User.objects.all().order_by('date_joined'),
        })
        return context
