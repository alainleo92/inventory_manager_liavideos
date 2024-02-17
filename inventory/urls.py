from django.urls import path
from .views import (
    Items,  
    EditItem, 
    DeleteItem, 
    Dashboard,
    Eventos, 
    EditEvento, 
    DeleteEvento, 
    Check_Evento)

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('items/', Items.as_view(), name='items'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('event/<int:event_id>', Check_Evento.as_view(), name='event'),
    path('events/', Eventos.as_view(), name='events'),
    path('edit-event/<int:pk>', EditEvento.as_view(), name='edit-event'),
    path('delete-event/<int:pk>', DeleteEvento.as_view(), name='delete-event'),
]