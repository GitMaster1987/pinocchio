from django.shortcuts import render

# Create your views here.
# Авторизация пользователя
def login(request):
   

    return render(request, 'users/login.html')

# Регистрация пользователя
def register(request):
   
    return render(request, 'users/registration.html')

# Выход
def logout(request):
   
    return render(request, 'users/registration.html')