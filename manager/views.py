from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, JsonResponse
from django.db.models import Sum, Count, F
from main.models import Categories, Products
from manager.forms import ProductForm
from orders.models import Order, OrderItem

# from django.views.decorators.http import require_POST


def group_required(groups):
    def check_user_group(user):
        return user.groups.filter(name__in=groups).exists() or user.is_superuser

    return user_passes_test(check_user_group)


@group_required(["Manager"])  # Разрешить доступ только группе "Manager"
def index(request):
    # Total number of orders
    total_orders = Order.objects.count()

    # Total revenue from orders (sum of prices and quantities for all order items)
    total_revenue = (
        OrderItem.objects.aggregate(total=Sum(F("price") * F("quantity")))["total"] or 0
    )

    # Most popular product based on order item quantity
    popular_product = (
        OrderItem.objects.values("product__name")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")
        .first()
    )
    popular_product_name = (
        popular_product["product__name"] if popular_product else "Нет данных"
    )

    # Latest orders (e.g., 10 most recent orders)
    latest_orders = Order.objects.prefetch_related("orderitem_set").order_by(
        "-created_timestamp"
    )[:10]
    return render(
        request,
        "manager/index.html",
        {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "popular_product_name": popular_product_name,
            "latest_orders": latest_orders,
        },
    )


@group_required(["Manager"])  # Разрешить доступ только группе "Manager"
def get_processing_orders(request):
    orders_in_processing = Order.objects.filter(status="В обработке")
    count_order = Order.objects.filter(status="В обработке").count()
    context = {"orders": orders_in_processing, "count_order": count_order}
    return render(request, "manager/processing_orders.html", context)


# Просмотр информации по заказу
@group_required(["Manager"])
def view_orders(request, order_id):
    # Получаем заказ по ID или возвращаем 404
    order = get_object_or_404(Order, id=order_id)

    # Получаем все позиции (блюда), связанные с заказом
    order_items = OrderItem.objects.filter(order=order)

    # Считаем общую сумму заказа
    total_price = sum(item.price * item.quantity for item in order_items)

    # Считаем общее количество товаров
    total_quantity = sum(item.quantity for item in order_items)

    # Статус оплаты
    status_payment = ""
    if order.payment_on_get:
        status_payment = "Оплата после получения"
    elif order.is_paid:
        status_payment = "Заказ оплачен картой"

    context = {
        # "order_id": order_id,
        "order": order,  # Заказ
        "order_items": order_items,  # Список блюд
        "total_price": total_price,  # Общая сумма заказа
        "total_quantity": total_quantity,  # Общее количество блюд
        "status_payment": status_payment,  # Статус оплаты заказа
    }

    return render(request, "manager/view_order.html", context)


# Удаление существующего заказа
@group_required(["Manager"])
def remove_orders(request):
    if request.method == "POST":  # Indentation for the POST block is correct
        # Получаем `order_id` из тела запроса
        order_id = request.POST.get("order_id")

        if not order_id:
            return JsonResponse({"error": "ID заказа не передан."}, status=400)

        # Находим заказ или возвращаем 404
        order = get_object_or_404(Order, id=order_id)
        order.delete()  # Удаляем заказ

        return JsonResponse({"message": "Заказ успешно удалён."})

    # This return should be outside the if block
    return JsonResponse(
        {"error": "Удаление доступно только через POST-запрос."}, status=405
    )


# ''' Редактирование заказа пользователя '''
@group_required(["Manager"])
def edit_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    # Получаем все позиции (блюда), связанные с заказом
    order_items = OrderItem.objects.filter(order=order)
    # Считаем общую сумму заказа
    total_price = sum(item.price * item.quantity for item in order_items)
    # Считаем общее количество товаров
    total_quantity = sum(item.quantity for item in order_items)
    # Список наших блюд, для модального окна
    products = Products.objects.all()

    context = {
        "order": order,
        "order_items": order_items,  # Список блюд
        "total_price": total_price,  # Общая сумма заказа
        "total_quantity": total_quantity,  # Общее количество блюд
        "products": products,
        "added_product_ids": [
            item.product.id for item in order_items
        ],  # Список ID добавленных блюд
        # 'formset': formset
    }

    return render(request, "manager/edit_order.html", context)


@group_required(["Manager"])
def order_quantity_change(request):

    order_id = request.POST.get("order_id")
    quantity = request.POST.get("quantity")

    order = OrderItem.objects.get(id=order_id)

    order.quantity = quantity
    order.save()

    return JsonResponse({"success": True})


@group_required(["Manager"])
def order_remove_cart(request):
    order_id = request.POST.get("order_id")
    order = OrderItem.objects.get(id=order_id)
    order.delete()

    return JsonResponse({"success": True})


# Добавление нового товара
@group_required(["Manager"])
def add_order_item(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity"))

    # Найдите продукт
    product = get_object_or_404(Products, pk=product_id)

    # Создайте новый элемент заказа
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        name=product.name,  # Сохраняем имя продукта
        price=product.price,
    )
    # Вернуться на страницу детализированного заказа (или на нужную вам страницу)
    return redirect(request.META["HTTP_REFERER"])


# Подтверждаем заказ пользователя
@group_required(["Manager"])
def confirm_order(request):
    if request.method == "POST":
        # Получаем данные из POST-запроса
        order_id = request.POST.get("order_id")
        order_date = request.POST.get("dateOrder")

        # Проверка на наличие даты
        if not order_date:
            raise Http404("Страница не найдена")

        # Преобразуем дату из строки в объект datetime
        try:
            order_date_obj = datetime.strptime(
                order_date, "%Y-%m-%dT%H:%M"
            )  # Формат datetime-local
        except ValueError:
            raise Http404("Страница не найдена")

        # Получаем заказ по ID
        order = get_object_or_404(Order, id=order_id)

        # Обновляем поля заказа
        order.order_date = order_date_obj
        order.status = "Подтвержден"
        order.save()  # Сохраняем изменения
        # Перенаправляем на страницу заказов
        return redirect("manager:processing_orders")

    raise Http404("Страница не найдена")


# Список подтвержденных заказов
@group_required(["Manager"])  # Разрешить доступ только группам "Chefs" и "Manager"
def confirms_order(request):
    orders_confirms = Order.objects.filter(status="Подтвержден")
    count_order = Order.objects.filter(status="Подтвержден").count()
    context = {"orders": orders_confirms, "count_order": count_order}
    return render(request, "manager/confirms_order.html", context)


# Возвращаем заказ в обработку
@group_required(["Manager"])
def return_processing(request, order_id):
    # Получаем заказ по ID или возвращаем 404
    order = get_object_or_404(Order, id=order_id)

    order.status = "В обработке"  # Меняем статус заказа

    order.order_date = None  # Очищаем дату подтвержденного заказа

    order.save()  # Сохраняем изменения

    # Вернуться на страницу детализированного заказа (или на нужную вам страницу)
    return redirect(request.META["HTTP_REFERER"])


# Список блюд для сайта
@group_required(["Manager"])
def view_products(request):
    products = Products.objects.filter(show=True)
    context = {"products": products}
    return render(request, "manager/view_products.html", context)


# Метод редактирования блюда на сайте
@group_required(["Manager"])
def edit_product(request, product_id):
    # Fetch the product by its ID
    product = get_object_or_404(Products, id=product_id)

    if request.method == "POST":
        # Update the product fields with the submitted data
        product.name = request.POST.get("name", product.name)
        product.description = request.POST.get("description", product.description)
        product.price = request.POST.get("price").replace(",", ".")
        product.discount = request.POST.get("discount", "0.00").replace(",", ".")
        product.show = (
            "show" in request.POST
        )  # Checkbox values are checked only if present in the POST data

        # Update the category
        category_id = request.POST.get("category")
        if category_id:
            product.category_id = category_id

        # Update the image if a new file is uploaded
        if request.FILES.get("image"):
            product.image = request.FILES["image"]

        # Save the changes to the database
        product.save()

        return redirect("manager:view_products")  # Adjust URL name as needed

    # Render the edit form if the request is not POST
    categories = Categories.objects.all()  # Retrieve all categories for dropdown
    return render(
        request,
        "manager/edit_product.html",
        {"product": product, "categories": categories},
    )


@group_required(["Manager"])
def add_to_stop_list(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if not product_id:
            return JsonResponse({"error": "ID продукта не передан."}, status=400)

        product = get_object_or_404(Products, id=product_id)
        product.show = False  # Set `show` to False to hide it
        product.save()

        return JsonResponse(
            {"message": f"Продукт '{product.name}' добавлен в стоп-лист."}
        )
    return JsonResponse({"error": "Недопустимый метод запроса."}, status=405)

@group_required(["Manager"])
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("manager:view_products")  # Redirect to the list of products
    else:
        form = ProductForm()
    categories = Categories.objects.all()  # Retrieve categories for dropdown
    return render(request, "manager/add_product.html", {"form": form, "categories": categories})
