from django.urls import path
from user_accounts.views import LoginView, LogoutView, RegisterView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('userprofile/', ProfileView.as_view(), name='profile'), 
]