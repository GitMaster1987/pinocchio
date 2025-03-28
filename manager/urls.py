from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns = [
    # ''' MANAGER '''
    path("", views.index, name="index"),
    path("processing_orders/", views.get_processing_orders, name="processing_orders"),
]
