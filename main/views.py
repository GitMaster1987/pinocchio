from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        "title": "Пиноккио - Пицца, которая не оставит вас равнодушным",
    }
    return render(request, "main/index.html", context)