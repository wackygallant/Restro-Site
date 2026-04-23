from rest_framework import viewsets

from api.serializers import BookingsSerializer, MenuCategoriesSerializer, MenuItemsSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from menu.models import MenuCategories, MenuItems
from booking.models import Booking

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