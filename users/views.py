from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.mail import send_mail
from carts.models import Cart
from users.forms import PasswordResetRequestForm, UserLoginForm, UserRegistrationForm
from users.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


# Авторизация пользователя
def login(request):

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            # Если пользователь не авторизирован, нужно для корзины
            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                # Переназначаем сессионный ключ
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user, session_key=None)
                # Получаем URL, на который пользователь пытался зайти (если он есть)
                next_url = request.GET.get("next")
                # Если URL есть, перенаправляем на него, иначе на страницу journal:index
                if next_url:
                    return HttpResponseRedirect(reverse(next_url))
                else:
                    return HttpResponseRedirect(reverse("main:index"))
    else:
        if request.user.is_authenticated:
            return redirect(reverse("main:index"))
        else:
            form = UserLoginForm()

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context)


# Регистрация пользователя
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # Если пользователь прошел регистрацию, нужно для корзины
            session_key = request.session.session_key
            
            user = form.instance
            auth.login(request, user)
            # Переназначаем сессионный ключ
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "users/register.html", context)


# Выход
@login_required
def logout(request):
    auth.logout(request)    
    return redirect(reverse("main:index"))


# Сброс пароля пользователя
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                protocol = "https" if request.is_secure() else "http"
                domain = request.get_host()
                reset_url = reverse(
                    "user:password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
                full_url = f"{protocol}://{domain}{reset_url}"
                mail_subject = "Сброс пароля"
                message = render_to_string(
                    "users/resset/password_reset_email.html",
                    {
                        "user": user,
                        "protocol": protocol,
                        "domain": domain,
                        "uid": uid,
                        "token": token,
                        "reset_url": full_url,
                    },
                )
                send_mail(
                    mail_subject,
                    message,
                    "meetnight1027@yandex.ru",
                    [email],
                    fail_silently=False,
                )
                return redirect("user:password_reset_done")
            except User.DoesNotExist:
                form.add_error("email", "Пользователь с таким email не найден.")
    else:
        form = PasswordResetRequestForm()
    return render(request, "users/resset/password_reset.html", {"form": form})


def password_reset_confirm(request, uidb64=None, token=None):
    if uidb64 is not None and token is not None:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("user:password_reset_complete")
            else:
                form = SetPasswordForm(user)
            return render(
                request, "users/resset/password_reset_confirm.html", {"form": form}
            )
        else:
            return render(request, "users/resset/password_reset_invalid.html")


def password_reset_complete(request):
    return render(request, "users/resset/password_reset_complete.html")
