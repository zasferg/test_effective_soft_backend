from django.contrib import admin
from .models import Dishes, Orders


@admin.register(Dishes)
class DishesAdmin(admin.ModelAdmin):
    list_display = ("dish", "price")
    search_fields = ("dish",)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("table_number", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("table_number",)
    date_hierarchy = "created_at"
