from django.contrib import admin
from django.contrib.auth.models import Group
from carts.admin import CartTabAdmin
from users.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", "phone_number"]
    list_filter = ["username", "first_name", "last_name", "email", "phone_number"]
    filter_horizontal = ["groups"]  # Добавляем горизонтальный фильтр для групп

    inlines = [CartTabAdmin,]
