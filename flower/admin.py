from django.contrib import admin

from .models import Bouquet, Consultation, Occasions, Order, PromoCode


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ["name", "height", "width", "description", "structure", "image", "price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "bouquet",
        "first_name",
        "address",
        "phone_number",
        "date_register",
        "date_deliver",
        "status",
        "total_price",
    ]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "phone_number", "confirmation", "date_statement"]


@admin.register(Occasions)
class OccasionsAdmin(admin.ModelAdmin):
    list_display = ["description"]
    filter_horizontal = ["bouquets"]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ["promo_code", "procent_promo", "is_active"]
