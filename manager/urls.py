from django.urls import path
from manager import views
from manager.views import (
    ManagerDashboardView,
    ProcessingOrdersView,
    ViewOrderDetailView,
    RemoveOrderView,
    EditOrderView,
    OrderQuantityChangeView,
    OrderRemoveCartView,
    AddOrderItemView,
    ConfirmOrderView,
    ConfirmsOrderListView,
)

app_name = "manager"

urlpatterns = [
    # ''' MANAGER '''
    path("", ManagerDashboardView.as_view(), name="index"),
    path(
        "processing_orders/", ProcessingOrdersView.as_view(), name="processing_orders"
    ),
    path("view_orders/<int:pk>/", ViewOrderDetailView.as_view(), name="view_orders"),
    # Удаление заказа
    path("remove_orders/", RemoveOrderView.as_view(), name="remove_orders"),
    # '''Edit-Order'''
    path("edit_order/<int:pk>/", EditOrderView.as_view(), name="edit_order"),
    path("order_quantity_change/", OrderQuantityChangeView.as_view(), name="order_quantity_change"),
    path("order_remove_cart/", OrderRemoveCartView.as_view(), name="order_remove_cart"),
    path("add_order_item/<int:order_id>/", AddOrderItemView.as_view(), name="add_order_item"),
    path("confirm_order/", ConfirmOrderView.as_view(), name="confirm_order"),
    # '''Confirms-Order'''
    path("confirms_order/", ConfirmsOrderListView.as_view(), name="confirms_order"),
    # '''Возвращаем в обработку'''
    path(
        "return_processing/<int:order_id>/",
        views.return_processing,
        name="return_processing",
    ),
    # '''Список наших блюд'''
    path("view_products/", views.view_products, name="view_products"),
    # '''Редактирование блюда''
    path("edit_product/<int:product_id>/", views.edit_product, name="edit_product"),
    # '''Добовление блюда в стоплист''
    path("add_to_stop_list/", views.add_to_stop_list, name="add_to_stop_list"),
    # '''Добовление нового блюда''
    path("add_product/", views.add_product, name="add_product"),
]
