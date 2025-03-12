from django.urls import path
from users import views
from django.views.generic import TemplateView
app_name = 'users'

urlpatterns = [
    # ''' USERS '''
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    # Сброс пароля пользователя
    # path("resset_password/", views.resset_password, name="resset_password"),
    # Сброс пароля пользователя
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset_done/', TemplateView.as_view(template_name='users/resset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]
