from django.urls import path
from .views import ShiftListView, ShiftCreateView, ShiftDetailView, ShiftCloseView

app_name = 'shifts'

urlpatterns = [
    path('', ShiftListView.as_view(), name='shift_list'),
    path('create/', ShiftCreateView.as_view(), name='shift_create'),
    path('<int:pk>/', ShiftDetailView.as_view(), name='shift_detail'),
    path('<int:pk>/close/', ShiftCloseView.as_view(), name='shift_close'),
]