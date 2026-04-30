from rest_framework import viewsets

from api.serializers import BookingsSerializer, MenuCategoriesSerializer, MenuItemsSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from menu.models import MenuCategories, MenuItems
from booking.models import Booking
from order.models import Order, OrderItem

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["MenuCategory(s)"])
class MenuCategoriesViewset(viewsets.ModelViewSet):
    queryset = MenuCategories.objects.all()
    serializer_class = MenuCategoriesSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=["Menu(s)"])
class MenuItemsViewset(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=["Booking(s)"])
class BookingViewset(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=["Order(s)"])
class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=["OrderItem(s)"])
class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]