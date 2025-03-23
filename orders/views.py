from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Оформление заказа пользователя
@login_required
def create_order(request):
    pass
