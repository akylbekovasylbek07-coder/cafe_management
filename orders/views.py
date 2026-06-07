from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem
from shifts.models import Shift
from .forms import OrderForm, OrderItemForm


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.select_related('table', 'shift').all()
        
        # Фильтры
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STATUS_CHOICES'] = Order.STATUS_CHOICES
        return context


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderItemForm()
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, есть ли открытая смена
        open_shift = Shift.get_open_shift()
        if not open_shift:
            messages.error(request, 'Сначала откройте смену!')
            return redirect('orders:order_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Проверяем, нет ли уже открытого заказа за этим столом
        existing = Order.objects.filter(
            table=form.cleaned_data['table'],
            status='open'
        ).first()
        
        if existing:
            messages.error(
                self.request, 
                f'У стола {form.cleaned_data["table"].number} уже есть открытый заказ!'
            )
            return redirect('orders:order_list')
        
        open_shift = Shift.get_open_shift()
        form.instance.shift = open_shift
        
        messages.success(self.request, 'Заказ успешно создан!')
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')

    def dispatch(self, request, *args, **kwargs):
        order = self.get_object()
        
        # Оплаченный заказ нельзя редактировать
        if order.status == 'paid':
            messages.error(request, 'Оплаченный заказ нельзя редактировать!')
            return redirect('orders:order_detail', pk=order.pk)
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Заказ успешно изменён!')
        return super().form_valid(form)


class OrderCloseView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        if order.status == 'paid':
            messages.error(request, 'Этот заказ уже оплачен!')
            return redirect('orders:order_detail', pk=order.pk)
        
        order.status = 'paid'
        order.save()
        
        messages.success(request, f'Заказ #{order.id} успешно оплачен!')
        return redirect('orders:order_detail', pk=order.pk)


class OrderItemAddView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        if order.status != 'open':
            messages.error(request, 'В оплаченный заказ нельзя добавлять товары!')
            return redirect('orders:order_detail', pk=order.pk)
        
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            
            # Проверяем, есть ли уже такая позиция
            existing = OrderItem.objects.filter(
                order=order,
                dish=form.cleaned_data['dish']
            ).first()
            
            if existing:
                existing.quantity += form.cleaned_data['quantity']
                existing.save()
            else:
                order_item.save()
            
            messages.success(request, 'Товар добавлен в заказ!')
        else:
            messages.error(request, 'Ошибка при добавлении товара')
        
        return redirect('orders:order_detail', pk=order.pk)


class OrderItemRemoveView(LoginRequiredMixin, View):
    def post(self, request, order_pk, item_pk):
        order = get_object_or_404(Order, pk=order_pk)
        
        if order.status != 'open':
            messages.error(request, 'В оплаченный заказ нельзя удалять товары!')
            return redirect('orders:order_detail', pk=order_pk)
        
        item = get_object_or_404(OrderItem, pk=item_pk, order=order)
        item.delete()
        
        messages.success(request, 'Товар удалён из заказа!')
        return redirect('orders:order_detail', pk=order_pk)