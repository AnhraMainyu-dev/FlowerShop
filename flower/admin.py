from django.contrib import admin
from .models import Bouquet, Order, Consultation


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ["name", "height", "width", "description", 'structure', "image", "price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['bouquet', 'first_name', 'address', 'phone_number', 'date_register', 'date_deliver', 'status']
    

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'phone_number', 'confirmation', 'date_statement']