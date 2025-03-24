from django.views.generic import TemplateView
from main.models import Banner, Categories, Products, Chefs

class IndexView(TemplateView):
    template_name = "main/index.html"  # Указываем шаблон для рендера

    # Метод для передачи контекста
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пиноккио - Пицца, которая не оставит вас равнодушным"
        context["banners"] = Banner.objects.all()
        context["categories"] = Categories.objects.all()
        context["products"] = Products.objects.filter(show=True).order_by("price")
        context["chefs"] = Chefs.objects.all()
        return context