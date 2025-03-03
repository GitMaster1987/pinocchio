from django.contrib import admin
from main.models import Nav, Banner, Categories, Products, Chefs

# Register your models here.
admin.site.register(Nav)


class BannerModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)

admin.site.register(Banner, BannerModelAdmin)

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Chefs)
