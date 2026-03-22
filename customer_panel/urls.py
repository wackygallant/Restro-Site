from django.urls import path

from customer_panel.views import HomePage, AboutPage
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
]