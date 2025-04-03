from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
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


@method_decorator(group_required(["Manager"]), name="dispatch")
class ManagerDashboardView(TemplateView):
    template_name = "manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total number of orders
        context["total_orders"] = Order.objects.count()

        # Total revenue from orders (sum of prices and quantities for all order items)
        context["total_revenue"] = (
            OrderItem.objects.aggregate(total=Sum(F("price") * F("quantity")))["total"]
            or 0
        )

        # Most popular product based on order item quantity
        popular_product = (
            OrderItem.objects.values("product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")
            .first()
        )
        context["popular_product_name"] = (
            popular_product["product__name"] if popular_product else "Нет данных"
        )

        # Latest orders (e.g., 10 most recent orders)
        context["latest_orders"] = Order.objects.prefetch_related("orderitem_set").order_by(
            "-created_timestamp"
        )[:10]

        return context

# Список новых заказов
@method_decorator(group_required(["Manager"]), name="dispatch")
class ProcessingOrdersView(ListView):
    model = Order
    template_name = "manager/processing_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Filter orders with the status "В обработке"
        return Order.objects.filter(status="В обработке")

    def get_context_data(self, **kwargs):
        # Add additional context for the count of orders
        context = super().get_context_data(**kwargs)
        context["count_order"] = self.get_queryset().count()
        return context


# Просмотр информации по заказу
@method_decorator(group_required(["Manager"]), name="dispatch")
class ViewOrderDetailView(DetailView):
    model = Order
    template_name = "manager/view_order.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get related order items
        order_items = OrderItem.objects.filter(order=self.object)

        # Calculate total price and total quantity
        total_price = sum(item.price * item.quantity for item in order_items)
        total_quantity = sum(item.quantity for item in order_items)

        # Determine payment status
        if self.object.payment_on_get:
            status_payment = "Оплата после получения"
        elif self.object.is_paid:
            status_payment = "Заказ оплачен картой"
        else:
            status_payment = "Не оплачено"

        # Add custom context
        context["order_items"] = order_items
        context["total_price"] = total_price
        context["total_quantity"] = total_quantity
        context["status_payment"] = status_payment

        return context


# Удаление существующего заказа
@method_decorator(group_required(["Manager"]), name="dispatch")
class RemoveOrderView(View):
    def post(self, request, *args, **kwargs):
        # Get `order_id` from the request POST data
        order_id = request.POST.get("order_id")

        if not order_id:
            return JsonResponse({"error": "ID заказа не передан."}, status=400)

        # Find the order or return a 404 error
        order = get_object_or_404(Order, id=order_id)
        order.delete()  # Delete the order

        return JsonResponse({"message": "Заказ успешно удалён."})

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Удаление доступно только через POST-запрос."}, status=405
        )


# ''' Редактирование заказа пользователя '''
@method_decorator(group_required(["Manager"]), name="dispatch")
class EditOrderView(DetailView):
    model = Order
    template_name = "manager/edit_order.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get related order items
        order_items = OrderItem.objects.filter(order=self.object)

        # Calculate total price and total quantity
        total_price = sum(item.price * item.quantity for item in order_items)
        total_quantity = sum(item.quantity for item in order_items)

        # List of all products for modal selection
        products = Products.objects.all()

        # Prepare context data
        context["order_items"] = order_items
        context["total_price"] = total_price
        context["total_quantity"] = total_quantity
        context["products"] = products
        context["added_product_ids"] = [item.product.id for item in order_items]

        return context


# Изменение кол-ва блюд в заказе
@method_decorator(group_required(["Manager"]), name="dispatch")
class OrderQuantityChangeView(View):
    def post(self, request, *args, **kwargs):
        # Get order item ID and new quantity from POST data
        order_id = request.POST.get("order_id")
        quantity = request.POST.get("quantity")

        if not order_id or not quantity:
            return JsonResponse({"error": "order_id и quantity обязательны."}, status=400)

        # Get the specific order item or return 404 if not found
        order_item = get_object_or_404(OrderItem, id=order_id)

        # Update the quantity
        try:
            order_item.quantity = int(quantity)
            order_item.save()
        except ValueError:
            return JsonResponse({"error": "Количество должно быть числом."}, status=400)

        return JsonResponse({"success": True})

# Удаление блюда из заказа пользлвателя
@method_decorator(group_required(["Manager"]), name="dispatch")
class OrderRemoveCartView(View):
    def post(self, request, *args, **kwargs):
        # Get order item ID from POST data
        order_id = request.POST.get("order_id")

        if not order_id:
            return JsonResponse({"error": "ID заказа не передан."}, status=400)

        # Get the order item or return 404
        order_item = get_object_or_404(OrderItem, id=order_id)

        # Delete the order item
        order_item.delete()

        return JsonResponse({"success": True})

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Удаление доступно только через POST-запрос."}, status=405
        )


# Добавление нового товара в заказ пользователя
@method_decorator(group_required(["Manager"]), name="dispatch")
class AddOrderItemView(View):
    def post(self, request, order_id, *args, **kwargs):
        # Retrieve the order using `order_id`
        order = get_object_or_404(Order, pk=order_id)

        # Get product_id and quantity from POST data
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:
            # If either value is missing, return an error
            return JsonResponse({"error": "Продукт или количество не переданы."}, status=400)

        try:
            quantity = int(quantity)  # Ensure quantity is a valid integer
        except ValueError:
            return JsonResponse({"error": "Количество должно быть числом."}, status=400)

        # Find the product or return 404 if not found
        product = get_object_or_404(Products, pk=product_id)

        # Create a new order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            name=product.name,  # Save the product's name
            price=product.price,  # Save the product's price
        )

        # Redirect back to the referring page
        return redirect(request.META.get("HTTP_REFERER", "/"))


# Подтверждаем заказ пользователя
@method_decorator(group_required(["Manager"]), name="dispatch")
class ConfirmOrderView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve data from POST request
        order_id = request.POST.get("order_id")
        order_date = request.POST.get("dateOrder")

        # Check if order_date is provided
        if not order_date:
            raise Http404("Страница не найдена")

        # Convert date string to datetime object
        try:
            order_date_obj = datetime.strptime(order_date, "%Y-%m-%dT%H:%M")  # datetime-local format
        except ValueError:
            raise Http404("Страница не найдена")

        # Retrieve the order by ID or raise 404
        order = get_object_or_404(Order, id=order_id)

        # Update order fields
        order.order_date = order_date_obj
        order.status = "Подтвержден"
        order.save()  # Save changes

        # Redirect to processing orders page
        return redirect("manager:processing_orders")

    def get(self, request, *args, **kwargs):
        raise Http404("Страница не найдена")


# Список подтвержденных заказов
@method_decorator(group_required(["Chefs", "Manager"]), name="dispatch")
class ConfirmsOrderListView(ListView):
    model = Order
    template_name = "manager/confirms_order.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Filter orders with status "Подтвержден"
        return Order.objects.filter(status="Подтвержден")

    def get_context_data(self, **kwargs):
        # Add additional context for the count of orders
        context = super().get_context_data(**kwargs)
        context["count_order"] = self.get_queryset().count()
        return context


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
