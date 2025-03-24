from django.views import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from main.models import Products



class CartAddView(View):
    """Добавление товара в корзину"""

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)

        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user, product=product)
            if carts.exists():
                cart = carts.first()
                cart.quantity += 1
                cart.save()
            else:
                Cart.objects.create(user=request.user, product=product, quantity=1)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()

            carts = Cart.objects.filter(
                session_key=request.session.session_key, product=product
            )
            if carts.exists():
                cart = carts.first()
                cart.quantity += 1
                cart.save()
            else:
                Cart.objects.create(
                    session_key=request.session.session_key,
                    product=product,
                    quantity=1,
                )

        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/carts.html", {"carts": user_cart}, request=request
        )
        response_data = {
            "message": "Товар добавлен в корзину",
            "cart_items_html": cart_items_html,
        }

        return JsonResponse(response_data)


class CartChangeView(View):
    """Изменение количества товара в корзине"""

    def post(self, request, *args, **kwargs):
        cart_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")
        cart = Cart.objects.get(id=cart_id)
        cart.quantity = quantity
        cart.save()

        updated_quantity = cart.quantity
        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/carts.html", {"carts": user_cart}, request=request
        )
        response_data = {
            "message": "Количество изменено!",
            "cart_items_html": cart_items_html,
            "quantity": updated_quantity,
        }

        return JsonResponse(response_data)


class CartRemoveView(View):
    """Удаление товара из корзины"""

    def post(self, request, *args, **kwargs):
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=cart_id)
        quantity = cart.quantity
        cart.delete()

        user_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            "carts/carts.html", {"carts": user_cart}, request=request
        )
        response_data = {
            "message": "Товар удален!",
            "cart_items_html": cart_items_html,
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)
