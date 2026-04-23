from rest_framework import serializers

from booking.models import Booking, TimeSlot
from menu.models import MenuCategories, MenuItems

class MenuCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategories
        fields = "__all__"

class MenuItemsSerializer(serializers.ModelSerializer):
    # category = MenuCategoriesSerializer()
    class Meta:
        model = MenuItems
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = MenuCategoriesSerializer(instance.category).data
        return data

class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"

class BookingsSerializer(serializers.ModelSerializer):
    # time_slot = TimeslotSerializer()
    class Meta:
        model = Booking
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["time_slot"] = TimeslotSerializer(instance.time_slot).data
        return data