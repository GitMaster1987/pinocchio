from django.urls import path
from django.views.generic import TemplateView
from users.views import (
    LoginView,
    RegisterView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    CheckEmailView,
    CheckUsernameView,
)

app_name = "users"

urlpatterns = [
    # Авторизация, регистрация и выход
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # Сброс пароля пользователя
    path("password_reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password_reset_done/",
        TemplateView.as_view(template_name="users/resset/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    
    # Проверка username
    path("check_username/", CheckUsernameView.as_view(), name="check_username"),
    # Проверка уникальности email
    path("check_email/", CheckEmailView.as_view(), name="check_email"),
]
