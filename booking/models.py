from django.db import models
from django.db.models import F, Sum

class TimeSlot(models.Model):
    # Example: 10:00 AM, 12:00 PM etc.
    # Unique so we don't create duplicate times
    time = models.TimeField(unique=True)

    def __str__(self):
        # Display in 12-hour format for humans
        return self.time.strftime("%I:%M %p")

class Booking(models.Model):
    # Name of the user booking
    user = models.CharField(max_length=100)
    # Booking date
    date = models.DateField()
    # Which time slot is booked
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    # How many tables this user books
    table_count = models.PositiveIntegerField()



