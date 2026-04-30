from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.viewsets import BookingViewset, MenuCategoriesViewset, MenuItemsViewset, OrderViewset, OrderItemViewset


router = DefaultRouter()

router.register('menu_categories', MenuCategoriesViewset, basename='menu_categories')
router.register('menu_items', MenuItemsViewset, basename='menu_items')
router.register('bookings', BookingViewset, basename='bookings')
router.register('orders', OrderViewset, basename='orders')
router.register('orderitems', OrderItemViewset, basename='orderitems')


urlpatterns = [
    path('', include(router.urls)),
]