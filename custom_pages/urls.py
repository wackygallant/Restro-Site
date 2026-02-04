from django.urls import path

from custom_pages.views import HomePage, AboutPage, BookingPage
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('booking/', BookingPage.as_view(), name='book'),

]