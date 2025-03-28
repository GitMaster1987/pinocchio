from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test

from orders.models import Order, OrderItem


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
    context = {"orders": orders_in_processing, "count_order": count_order}
    return render(request, "manager/processing_orders.html", context)


# Просмотр информации по заказу
@group_required("Manager")
def view_orders(request, order_id):
    # Получаем заказ по ID или возвращаем 404
    order = get_object_or_404(Order, id=order_id)

    # Получаем все позиции (блюда), связанные с заказом
    order_items = OrderItem.objects.filter(order=order)

    # Считаем общую сумму заказа
    total_price = sum(item.price * item.quantity for item in order_items)

    # Считаем общее количество товаров
    total_quantity = sum(item.quantity for item in order_items)

    context = {
        # "order_id": order_id,
        "order": order,  # Заказ
        "order_items": order_items,  # Список блюд
        "total_price": total_price,  # Общая сумма заказа
        "total_quantity": total_quantity,  # Общее количество блюд
    }

    return render(request, "manager/view_order.html", context)


# Удаление существующего заказа
def remove_orders(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Удаляем заказ
    order.delete()

    return redirect(request.META["HTTP_REFERER"])
