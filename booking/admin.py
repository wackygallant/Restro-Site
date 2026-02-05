from django.contrib import admin

from .models import TimeSlot, Booking

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time_slot', 'person_count')
    list_filter = ('date', 'time_slot', 'user')
