from django.contrib import admin
from main.models import Nav, Banner

# Register your models here.
admin.site.register(Nav)

class BannerModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)

admin.site.register(Banner, BannerModelAdmin)
