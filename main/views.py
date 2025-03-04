from django.shortcuts import render
from main.models import Banner, Categories, Products, Chefs

# Create your views here.
def index(request):
    banner = Banner.objects.all()
    categories = Categories.objects.all()
    products = Products.objects.all()
    chefs = Chefs.objects.all()
    context = {
        "title": "Пиноккио - Пицца, которая не оставит вас равнодушным",
        "banners": banner,
        'categories': categories,
        'products': products,
        'chefs': chefs
    }
    return render(request, "main/index.html", context)