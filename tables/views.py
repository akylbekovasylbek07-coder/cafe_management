from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Table
from .forms import TableForm


class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'

    def get_queryset(self):
        return Table.objects.all().order_by('number')


class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:table_list')

    def form_valid(self, form):
        messages.success(self.request, 'Стол успешно создан!')
        return super().form_valid(form)


class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:table_list')

    def form_valid(self, form):
        messages.success(self.request, 'Стол успешно изменён!')
        return super().form_valid(form)


class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('tables:table_list')

    def form_valid(self, form):
        messages.success(self.request, 'Стол успешно удалён!')
        return super().form_valid(form)
