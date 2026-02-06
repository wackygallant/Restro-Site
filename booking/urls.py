from django.urls import path
from .views import BookTableView

urlpatterns = [
    path('', BookTableView.as_view(), name='booking_page'),
]