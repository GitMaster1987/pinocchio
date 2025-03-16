from django.shortcuts import redirect, render

from carts.models import Cart
from main.models import Products


# Добавление в корзину
def cart_add(request, product_id): 
    product = Products.objects.get(id = product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user = request.user, product = product)
        # Если товар уже добавлен увеличиваем к-во на 1
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user = request.user, product=product, quantity = 1)
    
    return redirect(request.META['HTTP_REFERER'])


# Изменение корзины
def cart_change(request, product_id): ...


# Удаление из корзины
def cart_remove(request, product_id): ...
