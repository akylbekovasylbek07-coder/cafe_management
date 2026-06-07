from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['dish', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'shift', 'status', 'created_at', 'total_price']
    list_filter = ['status', 'shift']
    search_fields = ['id', 'table__number']
    ordering = ['-created_at']
    readonly_fields = ['table', 'shift', 'created_at', 'total_price']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'dish', 'quantity', 'subtotal']
    list_filter = ['order__status']
    search_fields = ['order__id', 'dish__name']
    ordering = ['-order__created_at']
