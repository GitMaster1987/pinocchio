from django.shortcuts import render
from main.models import Banner, Categories, Products

# Create your views here.
def index(request):
    banner = Banner.objects.all()
    categories = Categories.objects.all()
    products = Products.objects.all()
    context = {
        "title": "Пиноккио - Пицца, которая не оставит вас равнодушным",
        "banners": banner,
        'categories': categories,
        'products': products
    }
    return render(request, "main/index.html", context)