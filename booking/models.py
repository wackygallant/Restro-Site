from django.db import models
from django.contrib.auth.models import User

class TimeSlot(models.Model):
    # Example: 10:00 AM, 12:00 PM etc.
    # Unique so we don't create duplicate times
    time = models.TimeField(unique=True)

    def __str__(self):
        # Display in 12-hour format for humans
        return self.time.strftime("%I:%M %p")

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    phone_number = models.CharField(max_length=15, default='')
    booking_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    person_count = models.PositiveIntegerField(default=1)
    STATUS_CHOICES = {
        ('ended', 'Ended'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending')
    }
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking for {self.user} on {self.booking_date} at {self.time_slot} for {self.person_count} people."



