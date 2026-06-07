from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Shift
from orders.models import Order
from .forms import ShiftCloseForm


class ShiftListView(LoginRequiredMixin, ListView):
    model = Shift
    template_name = 'shifts/shift_list.html'
    context_object_name = 'shifts'

    def get_queryset(self):
        return Shift.objects.all().order_by('-opened_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_shift = Shift.get_open_shift()
        context['open_shift'] = open_shift
        return context


class ShiftCreateView(LoginRequiredMixin, CreateView):
    model = Shift
    template_name = 'shifts/shift_form.html'
    fields = []

    def form_valid(self, form):
        # Проверяем, нет ли уже открытой смены
        existing_open = Shift.get_open_shift()
        if existing_open:
            messages.error(self.request, f'Сначала закройте текущую смену #{existing_open.id}')
            return redirect('shifts:shift_list')
        
        messages.success(self.request, 'Смена успешно открыта!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shifts:shift_list')


class ShiftDetailView(LoginRequiredMixin, DetailView):
    model = Shift
    template_name = 'shifts/shift_detail.html'
    context_object_name = 'shift'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Все оплаченные заказы за эту смену
        context['paid_orders'] = Order.objects.filter(
            shift=self.object, 
            status='paid'
        ).order_by('-created_at')
        # Общая выручка
        context['total_revenue'] = sum(
            order.total_price for order in context['paid_orders']
        )
        return context


class ShiftCloseView(LoginRequiredMixin, View):
    def post(self, request, pk):
        shift = get_object_or_404(Shift, pk=pk)
        
        if not shift.is_open:
            messages.error(request, 'Эта смена уже закрыта')
            return redirect('shifts:shift_list')
        
        # Рассчитываем выручку за смену
        orders = Order.objects.filter(shift=shift, status='paid')
        total_revenue = sum(order.total_price for order in orders)
        
        with transaction.atomic():
            shift.is_open = False
            shift.closed_at = timezone.now()
            shift.save()
        
        messages.success(
            request, 
            f'Смена #{shift.id} закрыта! Выручка: {total_revenue} ₽'
        )
        return redirect('shifts:shift_detail', pk=shift.pk)