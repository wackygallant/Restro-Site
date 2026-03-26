from django.contrib import admin

from booking.models import TimeSlot, Booking

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_date', 'time_slot', 'person_count')
    list_filter = ('booking_date', 'time_slot')
    search_fields = ('user', 'email')