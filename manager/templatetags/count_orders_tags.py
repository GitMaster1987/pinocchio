from django import template
from orders.models import Order

register = template.Library()


@register.simple_tag()
def get_Count_Orders():
    return Order.objects.filter(status="В обработке").count()

@register.simple_tag()
def get_Count_Orders_Confirm():
    return Order.objects.filter(status="Подтвержден").count()