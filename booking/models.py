from django.db import models
from django.contrib.auth.models import User
import datetime

class TimeSlot(models.Model):
    # Example: 10:00 AM, 12:00 PM etc.
    # Unique so we don't create duplicate times
    time = models.TimeField(unique=True)

    def __str__(self):
        # Display in 12-hour format for humans
        return self.time.strftime("%I:%M %p")

class Booking(models.Model):
    STATUS_CHOICES = {
        ('ended', 'Ended'),
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending')
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=15, default='')
    booking_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='time_slots')
    person_count = models.PositiveIntegerField(default=1)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking for {self.user} on {self.booking_date} at {self.time_slot} for {self.person_count} people."

    def create_booking_id(self):
        """Create a unique booking ID in format BKG-YYYY-NNNN"""
        
        # Get current year
        current_year = datetime.datetime.now().year
        
        # Get the last order for this year to determine the next sequence number
        last_booking = Booking.objects.filter(
            booking_id__startswith=f'BKG-{current_year}-'
        ).order_by('-booking_id').first()
        
        if last_booking:
            # Extract the sequence number from the last order ID
            last_sequence = int(last_booking.booking_id.split('-')[-1])
            next_sequence = last_sequence + 1
        else:
            next_sequence = 1
        
        # Format with leading zeros (4 digits)
        self.booking_id = f'BKG-{current_year}-{next_sequence:04d}'
        return self.booking_id

