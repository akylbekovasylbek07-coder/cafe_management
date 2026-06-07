from django import forms
from .models import Order, OrderItem
from shifts.models import Shift
from tables.models import Table
from menu.models import Dish


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только активные столы
        self.fields['table'].queryset = Table.objects.filter(is_active=True)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']
        widgets = {
            'dish': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем только доступные блюда
        self.fields['dish'].queryset = Dish.objects.filter(is_available=True)