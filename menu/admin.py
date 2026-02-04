from django.contrib import admin

from menu.models import MenuCategories, MenuItems

# Register your models here.
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
    ordering = ('priority',)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_on_special', 'created_at', 'updated_at')
    list_filter = ('category', 'is_on_special')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

admin.site.register(MenuCategories, MenuCategoryAdmin)
admin.site.register(MenuItems, MenuItemAdmin)