from django.contrib import admin
from main.models import Nav, Banner, Categories, Products, Chefs

# Register your models here.
admin.site.register(Nav)


@admin.register(Banner)
class BannerModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "update_at")
    list_display = ["id", "title", "price", "created_at", "update_at"]
    list_editable = [
        "price",
    ]
    search_fields = [
        "title",
        "price",
        "created_at",
    ]
    list_filter = ["id", "title", "price", "created_at", "update_at"]


@admin.register(Categories)
class CategoriesModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]


@admin.register(Products)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "image_tag",
        "name",
        "price",
        "discount",
        "show",
        "category_title",
    ]
    readonly_fields = ("image_tag",)
    list_editable = [
        "discount",
    ]
    search_fields = [
        "name",
        "price",
        "description",
    ]
    list_filter = [
        "name",
        "price",
        "discount",
        "category__title",
    ]

    # Кастомный метод для отображения category.title
    def category_title(self, obj):
        return obj.category.title  # Возвращаем нужное значение

    category_title.short_description = "Категория"


@admin.register(Chefs)
class ChefsModelAdmin(admin.ModelAdmin):
    list_display = ["name", "lastName"]
    list_filter = ["name", "lastName"]
