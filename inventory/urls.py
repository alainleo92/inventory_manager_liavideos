from django.urls import path
from .views import (
    Items,  
    EditItem, 
    DeleteItem, 
    Dashboard)

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('items/', Items.as_view(), name='items'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
]