from django.db import models


class Shift(models.Model):
    """Рабочая смена"""
    opened_at = models.DateTimeField(auto_now_add=True, verbose_name="Открыта в")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Закрыта в")
    is_open = models.BooleanField(default=True, verbose_name="Открыта")

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"
        ordering = ['-opened_at']

    def __str__(self):
        if self.is_open:
            return f"Смена #{self.id} (открыта с {self.opened_at.strftime('%d.%m.%Y %H:%M')})"
        return f"Смена #{self.id} ({self.opened_at.strftime('%d.%m.%Y')} - {self.closed_at.strftime('%d.%m.%Y') if self.closed_at else 'закрыта'})"

    @classmethod
    def get_open_shift(cls):
        """Получить открытую смену"""
        return cls.objects.filter(is_open=True).first()
