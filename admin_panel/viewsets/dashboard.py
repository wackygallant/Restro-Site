from django.views import generic


class DashboardView(generic.TemplateView):
    template_name = 'admin_panel/dashboard.html'
