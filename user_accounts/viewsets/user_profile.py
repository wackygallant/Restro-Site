# Django Module Imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.shortcuts import render, redirect
from django.contrib import messages

# Model Imports
from user_accounts.models import ShippingAddress

# Form Imports
from user_accounts.formsets.shippingaddform import ShippingAddressForm

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'customer_panel/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        orders_qs = user.orders.all().order_by('-order_date').prefetch_related('order_items')
        bookings_qs = user.bookings.order_by('-booking_date')
        shipping_addresses = user.shipping_addresses.all()
        # orders_qs = Order.objects.filter(user=user.id).order_by('-order_date').prefetch_related('order_items')
    
        context.update({
            'user': user,
            'bookings': bookings_qs[:3],
            'orders': orders_qs[:3],
            'shipping_addresses': shipping_addresses,
            'booking_count': bookings_qs.count(),
            'order_count': orders_qs.count(),
        })
        return context

class AddShippingAddressView(LoginRequiredMixin, View):
    def post(self, request):
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.username = request.user
            address.save()
            messages.success(request, 'Address added successfully')
        else:
            messages.error(request, 'Please correct the errors below')
        return redirect('profile')

class EditShippingAddressView(LoginRequiredMixin,View):
    def get(self, request, pk):
        address = ShippingAddress.objects.get(id=pk, username=request.user)
        form = ShippingAddressForm(instance=address)
        return render(request, 'edit_shipping_address.html', {'form': form, 'address': address})
    
    def post(self, request, pk):
        address = ShippingAddress.objects.get(id=pk, username=request.user)
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully')
        else:
            messages.error(request, 'Please correct the errors below')
        return redirect('profile')

class DeleteShippingAddressView(LoginRequiredMixin, View):
    def post(self, request):
        address_id = request.POST.get('address_id')
        if address_id:
            try:
                address = ShippingAddress.objects.get(id=address_id, username=request.user)
                address.delete()
                messages.success(request, 'Address deleted successfully')
            except ShippingAddress.DoesNotExist:
                messages.error(request, 'Address not found')
        return redirect('profile')
