from django.urls import path
from .views import TableListView, TableCreateView, TableUpdateView, TableDeleteView

app_name = 'tables'

urlpatterns = [
    path('', TableListView.as_view(), name='table_list'),
    path('create/', TableCreateView.as_view(), name='table_create'),
    path('<int:pk>/update/', TableUpdateView.as_view(), name='table_update'),
    path('<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete'),
]