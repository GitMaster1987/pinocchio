from django import forms
from main.models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name", "description", "image", "price", "discount", "show", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название продукта"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Описание продукта"}),
            "image": forms.FileInput(attrs={"class": "form-control-file"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Цена"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Скидка (%)"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }