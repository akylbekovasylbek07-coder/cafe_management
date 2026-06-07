from django.db import models


class Table(models.Model):
    """Стол в кафе"""
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер стола")
    seats = models.PositiveIntegerField(verbose_name="Количество мест")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ['number']

    def __str__(self):
        return f"Стол №{self.number} ({self.seats} мест)"
