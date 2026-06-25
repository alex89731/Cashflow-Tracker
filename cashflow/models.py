from django.db import models
from django.utils import timezone

# --- Справочники ---

class Status(models.Model):
    """
    Модель для хранения статусов операций.
    Например: 'Бизнес', 'Личное', 'Налог'.
    """
    name = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name

class Type(models.Model):
    """
    Модель для хранения типов операций.
    Например: 'Пополнение', 'Списание'.
    """
    name = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name

class Category(models.Model):
    """
    Модель для хранения категорий операций. Каждая категория привязана к типу.
    Например, категория 'Маркетинг' относится к типу 'Списание'.
    """
    name = models.CharField("Название", max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name="Тип")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        # Категория должна быть уникальной в рамках своего типа
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.name} ({self.type.name})"

class Subcategory(models.Model):
    """
    Модель для хранения подкатегорий. Каждая подкатегория привязана к категории.
    Например, подкатегория 'Avito' относится к категории 'Маркетинг'.
    """
    name = models.CharField("Название", max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        # Подкатегория должна быть уникальной в рамках своей категории
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

# --- Основная модель ---

class CashFlow(models.Model):
    """
    Основная модель для хранения записей о движении денежных средств.
    """
    created_date = models.DateTimeField("Дата создания", default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    comment = models.TextField("Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "Запись о ДДС"
        verbose_name_plural = "Записи о ДДС"
        # Сортировка по умолчанию - от новых к старым
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.created_date.strftime('%d.%m.%Y')} - {self.type.name} - {self.amount}"
