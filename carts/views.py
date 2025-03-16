from django.shortcuts import render


# Добавление в корзину
def cart_add(request, product_id): ...


# Изменение корзины
def cart_change(request, product_id): ...


# Удаление из корзины
def cart_remove(request, product_id): ...
