from django.shortcuts import render
from django.views import View
from .models import Order

class OrderListView(View):
    def get(self, request):
        # orders = Order.objects.all()
        # username = get_username(request)
        return render(request, 'orders.html', {})