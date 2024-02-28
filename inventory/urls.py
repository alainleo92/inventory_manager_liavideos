from django.urls import path
from .views import Items, EditItem, DeleteItem

urlpatterns = [
    path('items/', Items.as_view(), name='items'),
    path('items/edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('items/delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
]