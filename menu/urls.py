from django.urls import path
from .views import DishListView, DishCreateView, DishUpdateView, DishDeleteView

app_name = 'menu'

urlpatterns = [
    path('', DishListView.as_view(), name='dish_list'),
    path('create/', DishCreateView.as_view(), name='dish_create'),
    path('<int:pk>/update/', DishUpdateView.as_view(), name='dish_update'),
    path('<int:pk>/delete/', DishDeleteView.as_view(), name='dish_delete'),
]