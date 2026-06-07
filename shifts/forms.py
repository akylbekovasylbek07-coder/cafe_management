from django import forms
from .models import Shift


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = []


class ShiftCloseForm(forms.Form):
    """Форма для закрытия смены"""
    pass