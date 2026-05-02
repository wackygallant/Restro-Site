from django.forms import ModelForm
from django.contrib.auth.models import User

class Admin_UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active', )