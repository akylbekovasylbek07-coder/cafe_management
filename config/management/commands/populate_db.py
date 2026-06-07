"""
Скрипт для быстрой установки тестовых данных
Запустите: python manage.py populate_db
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tables.models import Table
from menu.models import Dish
from shifts.models import Shift
from orders.models import Order, OrderItem
from decimal import Decimal


class Command(BaseCommand):
    help = 'Заполнить базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Создаём суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Суперпользователь "admin" создан'))
        else:
            self.stdout.write(self.style.WARNING('Суперпользователь "admin" уже существует'))

        # Создаём официанта
        if not User.objects.filter(username='waiter').exists():
            User.objects.create_user('waiter', 'waiter@example.com', 'waiter123')
            self.stdout.write(self.style.SUCCESS('Пользователь "waiter" создан'))
        else:
            self.stdout.write(self.style.WARNING('Пользователь "waiter" уже существует'))

        # Создаём столы
        tables_data = [
            {'number': 1, 'seats': 4},
            {'number': 2, 'seats': 6},
            {'number': 3, 'seats': 2},
            {'number': 4, 'seats': 4},
            {'number': 5, 'seats': 8},
        ]

        for table_data in tables_data:
            table, created = Table.objects.get_or_create(
                number=table_data['number'],
                defaults=table_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Стол №{table.number} создан'))

        # Создаём блюда
        dishes_data = [
            {
                'name': 'Борщ русский',
                'description': 'Традиционный русский борщ со сметаной и пампушками',
                'price': Decimal('250.00')
            },
            {
                'name': 'Пельмени домашние',
                'description': 'Домашние пельмени с мясом и маслом',
                'price': Decimal('320.00')
            },
            {
                'name': 'Оливье',
                'description': 'Классический салат оливье',
                'price': Decimal('280.00')
            },
            {
                'name': 'Цезарь с курицей',
                'description': 'Салат цезарь с куриной грудкой и пармезаном',
                'price': Decimal('350.00')
            },
            {
                'name': 'Бефстроганов',
                'description': 'Говядина по-строгановски со сметанным соусом',
                'price': Decimal('420.00')
            },
            {
                'name': 'Компот',
                'description': 'Домашний компот из свежих фруктов',
                'price': Decimal('120.00')
            },
            {
                'name': 'Чай чёрный',
                'description': 'Чёрный чай с лимоном',
                'price': Decimal('80.00')
            },
            {
                'name': 'Пирог с капустой',
                'description': 'Домашний пирог с капустой',
                'price': Decimal('150.00')
            },
        ]

        for dish_data in dishes_data:
            dish, created = Dish.objects.get_or_create(
                name=dish_data['name'],
                defaults=dish_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Блюдо "{dish.name}" созданo'))

        # Создаём открытую смену
        if not Shift.objects.filter(is_open=True).exists():
            shift = Shift.objects.create()
            self.stdout.write(self.style.SUCCESS(f'Смена #{shift.id} открыта'))
        else:
            self.stdout.write(self.style.WARNING('Смена уже открыта'))

        self.stdout.write(self.style.SUCCESS('\n✅ База данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS('\nДанные для входа:'))
        self.stdout.write(self.style.SUCCESS('  Администратор: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  Официант: waiter / waiter123'))