from django.db import models
from django.core.validators import MinValueValidator


class Dish(models.Model):
    """Блюдо из меню"""
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Цена"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступно")

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price} ₽"
