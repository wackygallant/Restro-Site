from django.shortcuts import render
from django.views import View
from order.models import OrderItems
from utils._utils import get_username

class OrderListView(View):
    def get(self, request):
        orders = OrderItems.objects.all()
        username = get_username(request)
        return render(request, 'orders.html', {'orders': orders, 'username': username})