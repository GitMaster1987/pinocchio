from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    # ''' USERS '''
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
]