from django.contrib import admin

from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "product", "quantity", "created_at"
    search_fields = "product", "quantity", "created_at"
    readonly_fields = ("created_at",)
    extra = 1


# Register your models here.
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "image_tag",
        "product_name",
        "quantity",
        "created_at",
    ]
    search_fields = ["user_display", "product", "quantity", "created_at"]
    list_filter = ["created_at", "user", "product__name"]

    # Кастомный метод для отображения product.name
    def product_name(self, obj):
        return obj.product.name  # Возвращаем нужное значение

    product_name.short_description = "Блюдо"

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
    user_display.short_description = "Пользователь"
