from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Bouquet(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    height = models.IntegerField(blank=True, null=True, verbose_name="Высота")
    width = models.IntegerField(blank=True, null=True, verbose_name="Ширина")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="bouquet/", verbose_name="Фото")
    structure = models.TextField(blank=True, verbose_name="Состав букета")
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Цена")

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    bouquet = models.ForeignKey(Bouquet, related_name="orders", verbose_name="Букет", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    address = models.CharField(max_length=100, verbose_name="Адрес")
    phone_number = PhoneNumberField(verbose_name="Телефон")
    date_register = models.DateTimeField(verbose_name="Дата создания заказа", auto_now_add=True)
    date_deliver = models.CharField(
        max_length=15,
        choices=[
            ("FA", "Как можно скорее"),
            ("MO", "10:00 - 12:00"),
            ("PM", "12:00 - 14:00"),
            ("BR", "14:00- 16:00"),
            ("PB", "16:00 - 18:00"),
            ("PM", "18:00 - 20:00"),
        ],
        db_index=True,
        blank=True,
        verbose_name="Время доставки",
    )
    status = models.CharField(
        max_length=25,
        choices=[("RG", "Зарегистрирован"), ("WD", "Ожидает доставки"), ("FO", "Доставлен")],
        default="RG",
        db_index=True,
        blank=True,
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.first_name} {self.date_register}"


class Consultation(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    phone_number = PhoneNumberField(verbose_name="Телефон")
    confirmation = models.BooleanField(default=False, verbose_name="Подтвердить")
    date_statement = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"

    def __str__(self):
        return f"{self.first_name} {self.phone_number}"


class Occasions(models.Model):
    description = models.CharField(max_length=50, verbose_name="Повод для подарка")
    bouquets = models.ManyToManyField(Bouquet, related_name="occasions", blank=True, verbose_name="Букет")

    class Meta:
        verbose_name = "Ситуация"
        verbose_name_plural = "Ситуации"

    def __str__(self):
        return self.description
