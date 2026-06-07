from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Dish
from .forms import DishForm


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'menu/dish_list.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.all().order_by('name')


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'menu/dish_form.html'
    success_url = reverse_lazy('menu:dish_list')

    def form_valid(self, form):
        messages.success(self.request, 'Блюдо успешно создано!')
        return super().form_valid(form)


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'menu/dish_form.html'
    success_url = reverse_lazy('menu:dish_list')

    def form_valid(self, form):
        messages.success(self.request, 'Блюдо успешно изменено!')
        return super().form_valid(form)


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    template_name = 'menu/dish_confirm_delete.html'
    success_url = reverse_lazy('menu:dish_list')

    def form_valid(self, form):
        messages.success(self.request, 'Блюдо успешно удалено!')
        return super().form_valid(form)