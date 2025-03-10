from pyexpat import model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import fields

from users.models import User


# Форма авторизации ===>
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control form-control-lg",
                "placeholder": "Имя пользователя",
                "required": True,
                "autocomplete": "off",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control form-control-lg",
                "placeholder": "Ваш пароль",
                "required": True,
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password"]


# Форма для регистрации пользователя
class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
        )

    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    phone_number = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()