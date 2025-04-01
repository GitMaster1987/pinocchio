from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns = [
    # ''' MANAGER '''
    path("", views.index, name="index"),
    path("processing_orders/", views.get_processing_orders, name="processing_orders"),
    path("view_orders/<int:order_id>/", views.view_orders, name="view_orders"),
    path("remove_orders/", views.remove_orders, name="remove_orders"),
    # '''Edit-Order'''
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('order_quantity_change/', views.order_quantity_change, name='order_quantity_change'),
    path('order_remove_cart/', views.order_remove_cart, name='order_remove_cart'),
    path('add_order_item/<int:order_id>/', views.add_order_item, name='add_order_item'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    # '''Confirms-Order'''
    path('confirms_order/', views.confirms_order, name='confirms_order'),
    # '''Возвращаем в обработку'''
    path('return_processing/<int:order_id>/', views.return_processing, name='return_processing'),
    # '''Список наших блюд'''
    path('view_products/', views.view_products, name='view_products'),
    # '''Редактирование блюда''
    path('edit_product/<int:product_id>', views.edit_product, name='edit_product'),
]
