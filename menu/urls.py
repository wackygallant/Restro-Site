from django.urls import path
from menu.views import Menu_Item_Detail, Menu_Page

urlpatterns = [
    path('', Menu_Page.as_view(), name='menu'),
    path('category/<slug:category_slug>/', Menu_Page.as_view(), name='category_filter'),
    path('item/<slug:item_slug>/', Menu_Item_Detail.as_view(), name='menu_item_detail'),
]