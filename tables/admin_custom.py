# Создаём кастомный админ для более удобного управления
from django.contrib import admin
from django.db.models import Sum
from .models import Table, Order


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'seats', 'is_active', 'active_orders']
    list_filter = ['is_active']
    search_fields = ['number']
    ordering = ['number']

    @admin.display(description='Активные заказы')
    def active_orders(self, obj):
        return Order.objects.filter(table=obj, status='open').count()


# Дополнительные настройки для Order в admin.py orders