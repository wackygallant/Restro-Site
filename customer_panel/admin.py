from django.contrib import admin
from customer_panel.models import Teams, Reviews

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rating')
    search_fields = ('first_name', 'last_name')
    list_filter = ('rating',)
