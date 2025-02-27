from django.shortcuts import render
from main.models import Banner

# Create your views here.
def index(request):
    banner = Banner.objects.all()

    context = {
        "title": "Пиноккио - Пицца, которая не оставит вас равнодушным",
        "banners": banner
    }
    return render(request, "main/index.html", context)