from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns = [
    # ''' MANAGER '''
    path("", views.index, name="index"),
]
