from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns = [
    # ''' MANAGER '''
    path("", views.index, name="index"),
    path("processing_orders/", views.get_processing_orders, name="processing_orders"),
    path("view_orders/<int:order_id>/", views.view_orders, name="view_orders"),
    path("remove_orders/<int:order_id>/", views.remove_orders, name="remove_orders"),
]
