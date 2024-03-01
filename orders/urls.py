from django.urls import path
from .views import Orders, EditOrder, DeleteOrder

urlpatterns = [
    path('orders/', Orders.as_view(), name='orders'),
    path('orders/edit-order/<int:pk>', EditOrder.as_view(), name='edit-order'),
    path('orders/delete-order/<int:pk>', DeleteOrder.as_view(), name='delete-order'),
    ]