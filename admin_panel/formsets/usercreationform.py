from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Admin_UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active')