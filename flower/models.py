from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Bouquet(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    heigth = models.IntegerField(verbose_name="Высота")
    weigth = models.IntegerField(verbose_name="Ширина")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="bouquet/", verbose_name="Фото")
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Цена")

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Эл.Почта")
    phone_number = PhoneNumberField(verbose_name="Телефон")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.bouquet}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ")
    bouquet = models.ForeignKey(Bouquet, related_name="order_items", on_delete=models.CASCADE, verbose_name="Детали")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Цена")

    class Meta:
        verbose_name = "Детали"
        verbose_name_plural = "Детали заказа"

    def __str__(self):
        return f"{self.bouquet} {self.order}"


class Consultation(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    phone_number = PhoneNumberField(verbose_name="Телефон")
    confirmation = models.BooleanField(default=False, verbose_name="Подтвердить")

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"

    def __str__(self):
        return f"{self.first_name} {self.phone_number}"
