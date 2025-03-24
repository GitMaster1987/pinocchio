from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from carts.models import Cart
from users.models import User
from users.forms import PasswordResetRequestForm, UserLoginForm, UserRegistrationForm


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        username = self.request.POST["username"]
        password = self.request.POST["password"]
        user = authenticate(username=username, password=password)
        session_key = self.request.session.session_key

        if user:
            auth_login(self.request, user)
            # Обновляем корзину для авторизованного пользователя
            if session_key:
                Cart.objects.filter(session_key=session_key).update(
                    user=user, session_key=None
                )
            # Перенаправляем на предыдущую страницу или главную
            next_url = self.request.GET.get("next")
            return HttpResponseRedirect(next_url or reverse("main:index"))

        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("main:index"))
        return super().get(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        form.save()
        session_key = self.request.session.session_key
        user = form.instance
        auth_login(self.request, user)
        # Обновляем корзину
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
        return HttpResponseRedirect(reverse("main:index"))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect(reverse("main:index"))


class PasswordResetRequestView(FormView):
    template_name = "users/resset/password_reset.html"
    form_class = PasswordResetRequestForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            protocol = "https" if self.request.is_secure() else "http"
            domain = self.request.get_host()
            reset_url = reverse(
                "user:password_reset_confirm", kwargs={"uidb64": uid, "token": token}
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
            return super().form_invalid(form)


class PasswordResetConfirmView(View):
    template_name = "users/resset/password_reset_confirm.html"

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("user:password_reset_complete")
            return render(request, self.template_name, {"form": form})

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)

        if default_token_generator.check_token(user, token):
            form = SetPasswordForm(user)
            return render(request, self.template_name, {"form": form})
        else:
            return render(request, "users/resset/password_reset_invalid.html")


class PasswordResetCompleteView(TemplateView):
    template_name = "users/resset/password_reset_complete.html"


class CheckEmailView(View):
    """Проверка уникальности email"""

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")
        is_unique = not User.objects.filter(
            email=email
        ).exists()  # Проверяем, уникален ли email
        return JsonResponse({"is_unique": is_unique})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Invalid request"}, status=400)


class CheckUsernameView(View):
    """Проверка уникальности username"""

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", "")
        is_unique = not User.objects.filter(username=username).exists()
        return JsonResponse({"is_unique": is_unique})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Invalid request"}, status=400)
