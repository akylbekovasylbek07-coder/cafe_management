from django.urls import path
from .views import (
    OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView,
    OrderCloseView, OrderItemAddView, OrderItemRemoveView
)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/close/', OrderCloseView.as_view(), name='order_close'),
    path('<int:pk>/items/add/', OrderItemAddView.as_view(), name='order_item_add'),
    path('<int:pk>/items/<int:item_pk>/remove/', OrderItemRemoveView.as_view(), name='order_item_remove'),
]