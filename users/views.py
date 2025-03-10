from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import UserLoginForm

# Create your views here.
# Авторизация пользователя
def login(request):
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                 # Получаем URL, на который пользователь пытался зайти (если он есть)
                next_url = request.GET.get('next')
            # Если URL есть, перенаправляем на него, иначе на страницу journal:index
                if next_url:
                    return HttpResponseRedirect(reverse(next_url))
                else:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        if request.user.is_authenticated:
           return redirect(reverse('main:index'))
        else: 
            form = UserLoginForm()
    
    context = {
        'form' : form,
    }

    return render(request, 'users/login.html', context)

# Регистрация пользователя
def register(request):
   
    return render(request, 'users/registration.html')

# Выход
@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))