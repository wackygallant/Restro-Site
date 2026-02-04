from django.urls import path
from .views import BookingPage

urlpatterns = [
    path('', BookingPage.as_view(), name='booking_page'),
]