from django.contrib.auth.mixins import AccessMixin

from django.shortcuts import redirect

from django.http import HttpRequest

class AdminLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        request : HttpRequest = request

        if request.user.is_authenticated and not request.user.is_anonymous:
            role = request.user.is_superuser or request.user.is_staff
            match role:
                case True:
                    return super().dispatch(request, *args, **kwargs)
                case _:
                    return redirect("home")
        else:
            return self.handle_no_permission()