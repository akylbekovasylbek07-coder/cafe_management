from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'seats', 'is_active']
    list_filter = ['is_active']
    search_fields = ['number']
    ordering = ['number']
