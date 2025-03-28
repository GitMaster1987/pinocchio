from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from orders.models import Order


def group_required(group_name):
    def in_group(user):
        return user.groups.filter(name=group_name).exists()

    return user_passes_test(in_group)


@group_required("Manager")  # Разрешить доступ только группе "Manager"
def index(request):
    return render(request, "manager/index.html")


@group_required("Manager")  # Разрешить доступ только группе "Manager"
def get_processing_orders(request):
    orders_in_processing = Order.objects.filter(status="В обработке")
    count_order = Order.objects.filter(status="В обработке").count()
    context = {
        "orders": orders_in_processing, 
        "count_order": count_order
    }
    return render(request, "manager/processing_orders.html", context)
