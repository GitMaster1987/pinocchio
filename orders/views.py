from ssl import AlertDescription
from django.http import JsonResponse, Http404
from django.db import transaction
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.contrib import messages
from carts.models import Cart
from carts.utils import get_user_carts
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


def create_order(request):
    if request.method == "POST":
        form = CreateOrderForm(data=request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        if form.cleaned_data["payment_on_get"] == "0":
                            payment_on_get = True
                            is_paid = False
                        else:
                            payment_on_get = False
                            is_paid = True
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data["phone_number"],
                            payment_on_get=payment_on_get,
                            is_paid=is_paid,
                        )
                        for cart_item in cart_items:
                            OrderItem.objects.create(
                                order=order,
                                product=cart_item.product,
                                name=cart_item.product.name,
                                price=cart_item.product.sell_price(),
                                quantity=cart_item.quantity,
                            )
                        cart_items.delete()

                        user_cart = get_user_carts(request)
                        cart_items_html = render_to_string(
                            "carts/carts.html", {"carts": user_cart}, request=request
                        )

                        return JsonResponse({
                            "message": "Заказ оформлен!",
                            "cart_items_html": cart_items_html,
                        }, json_dumps_params={"ensure_ascii": False})
            except ValidationError as e:
                return JsonResponse({"message": str(e)}, status=400)
        return JsonResponse({
            "message": "Некорректные данные",
            "errors": form.errors,
        }, status=400)
    else:
        raise Http404("Страница не найдена")