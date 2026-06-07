from django.contrib import admin
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available']
    list_filter = ['is_available']
    search_fields = ['name', 'description']
    ordering = ['name']
