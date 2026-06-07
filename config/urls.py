"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


def home_view(request):
    """Главная страница"""
    from shifts.models import Shift
    from orders.models import Order
    from tables.models import Table
    from datetime import date, timedelta
    
    open_shift = Shift.get_open_shift()
    open_orders = Order.objects.filter(status='open').count()
    total_tables = Table.objects.count()
    
    # Выручка за сегодня
    today = date.today()
    paid_orders_today = Order.objects.filter(
        status='paid',
        created_at__date=today
    )
    today_revenue = sum(order.total_price for order in paid_orders_today)
    
    context = {
        'open_shift': open_shift,
        'open_orders': open_orders,
        'total_tables': total_tables,
        'today_revenue': today_revenue,
    }
    return render(request, 'home.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('tables/', include('tables.urls')),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
    path('shifts/', include('shifts.urls')),
    
    # Авторизация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
