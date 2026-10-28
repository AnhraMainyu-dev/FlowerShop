from django.contrib import admin

from .models import Bouquet, Order, OrderItems


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ["name", "heigth", "weigth", "description", "image", "price"]


class TabularOrder(admin.TabularInline):
    model = OrderItems
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone_number"]
    inlines = [TabularOrder]
