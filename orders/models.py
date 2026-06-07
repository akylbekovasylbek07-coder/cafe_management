from django.db import models
from shifts.models import Shift
from tables.models import Table
from menu.models import Dish


class Order(models.Model):
    """Заказ клиента"""
    STATUS_CHOICES = [
        ("open", "Открыт"),
        ("paid", "Оплачен"),
        ("cancelled", "Отменён"),
    ]

    table = models.ForeignKey(Table, on_delete=models.PROTECT, verbose_name="Стол")
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, verbose_name="Смена")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} - Стол {self.table.number}"

    @property
    def total_price(self):
        """Общая стоимость заказа"""
        return sum(item.subtotal for item in self.items.all())

    def is_paid(self):
        """Проверка статуса оплаты"""
        return self.status == "paid"


class OrderItem(models.Model):
    """Позиция заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, verbose_name="Блюдо")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"

    @property
    def subtotal(self):
        """Стоимость позиции"""
        return self.quantity * self.dish.price
