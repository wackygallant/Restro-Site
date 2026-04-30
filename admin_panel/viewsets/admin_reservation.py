# Django Module Imports
from django.views import generic
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib import messages

# App Imports
from booking.models import Booking

class AdminReservationView(generic.ListView):
    model = Booking
    template_name = 'admin_panel/admin_all_reservation.html'
    context_object_name = 'reservations'
    paginate_by = 10
    
    def get_queryset(self):
        # 1. Base Queryset with optimizations
        queryset = Booking.objects.all().order_by("-booking_date")

        # 2. Get parameters from request
        search_query = self.request.GET.get('search')
        status_filters = self.request.GET.getlist('status')

        # 3. Apply logic conditionally
        if search_query:
            queryset = queryset.filter(
                Q(booking_id__icontains=search_query) | 
                Q(user__username__icontains=search_query)
            )

        if status_filters:
            queryset = queryset.filter(booking_status__in=status_filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = [choice[0] for choice in Booking.STATUS_CHOICES]
        return context


    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('reservation_id')
        status = request.POST.get('status')
        booking = Booking.objects.get(id=reservation_id)
        booking.booking_status = status
        booking.save()
        messages.success(request, f"Reservation for {booking.booking_id} status updated to {status}.")
        return redirect('admin_reservations')
