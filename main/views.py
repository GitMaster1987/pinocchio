from django.shortcuts import render
from main.models import Banner, Categories

# Create your views here.
def index(request):
    banner = Banner.objects.all()
    categories = Categories.objects.all()

    context = {
        "title": "Пиноккио - Пицца, которая не оставит вас равнодушным",
        "banners": banner,
        'categories': categories
    }
    return render(request, "main/index.html", context)