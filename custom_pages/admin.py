from django.contrib import admin
from custom_pages.models import Chefs, Testimonials

@admin.register(Chefs)
class ChefAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

@admin.register(Testimonials)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    search_fields = ('name',)
    list_filter = ('rating',)
