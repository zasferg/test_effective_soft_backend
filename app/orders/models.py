from typing import Any
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from orders.validators import validate_russian_characters


class Dishes(models.Model):
    """
    Модель для представления блюда.
    """

    dish = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        validators=[validate_russian_characters],
    )
    descr = models.TextField(
        max_length=255,
        null=False,
        blank=True,
        validators=[validate_russian_characters],
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["dish"]

    def __str__(self) -> str:
        return f"Блюдо: {self.dish}. Цена:{self.price}"


class Orders(models.Model):
    """
    Модель для представления заказа.
    """

    class Status(models.TextChoices):
        ОЖИДАЕТ = "Ожидает"
        ГОТОВ = "Готов"
        ОТМЕНЕН = "Отменен"

    table_number = models.IntegerField(
        null=False,
        validators=[MinValueValidator(0)],
    )
    items = models.ManyToManyField(
        Dishes,
        default=None,
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ОЖИДАЕТ,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Сохраняет заказ и пересчитывает общую стоимость.
        """
        super().save(*args, **kwargs)
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self) -> Decimal:
        """
        Вычисляет общую стоимость заказа, суммируя стоимость всех блюд.
        """
        total = Decimal(0.00)
        for item in self.items.all():
            total += item.price
        return total

    def __str__(self) -> str:
        return f"Заказ {self.id} для стола {self.table_number}"
