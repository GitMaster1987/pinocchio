from django.contrib import admin

from carts.admin import CartTabAdmin
from users.models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", "phone_number"]
    list_filter = ["username", "first_name", "last_name", "email", "phone_number"]

    inlines = [CartTabAdmin,]
