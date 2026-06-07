from django.contrib import admin
from .models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['id', 'opened_at', 'closed_at', 'is_open']
    list_filter = ['is_open']
    search_fields = ['id']
    ordering = ['-opened_at']
