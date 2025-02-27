from django import template
from main.models import Nav

register = template.Library()

@register.simple_tag()
def get_Menu():
    return Nav.objects.all()