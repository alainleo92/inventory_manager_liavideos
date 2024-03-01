from django.urls import path
from .views import Eventos, Check_Evento, EditEvento, DeleteEvento

urlpatterns = [
    path('events/', Eventos.as_view(), name='events'),
    path('events/event/<int:event_id>', Check_Evento.as_view(), name='event'),
    path('events/edit-event/<int:pk>', EditEvento.as_view(), name='edit-event'),
    path('events/delete-event/<int:pk>', DeleteEvento.as_view(), name='delete-event'),
]