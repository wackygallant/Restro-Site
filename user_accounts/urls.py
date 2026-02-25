from django.urls import path
from user_accounts.views import LoginView, LogoutView, RegisterView, ProfileView, AddShippingAddressView, EditShippingAddressView, DeleteShippingAddressView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('userprofile/', ProfileView.as_view(), name='profile'),
    path('add-shipping-address/', AddShippingAddressView.as_view(), name='add_shipping_address'),
    path('edit-shipping-address/<int:pk>/', EditShippingAddressView.as_view(), name='edit_shipping_address'),
    path('delete-shipping-address/', DeleteShippingAddressView.as_view(), name='delete_shipping_address'),
]