from django.contrib import admin
from django.urls import path
from .views import (
    Index, 
    SignUpView, 
    Items,  
    EditItem, 
    DeleteItem, 
    Dashboard, Orders,  
    EditOrder, 
    DeleteOrder, 
    Eventos, 
    EditEvento, 
    DeleteEvento, 
    Check_Evento)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('items/', Items.as_view(), name='items'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('orders/', Orders.as_view(), name='orders'),
    path('event/<int:event_id>', Check_Evento.as_view(), name='event'),
    path('edit-order/<int:pk>', EditOrder.as_view(), name='edit-order'),
    path('delete-order/<int:pk>', DeleteOrder.as_view(), name='delete-order'),
    path('events/', Eventos.as_view(), name='events'),
    path('edit-event/<int:pk>', EditEvento.as_view(), name='edit-event'),
    path('delete-event/<int:pk>', DeleteEvento.as_view(), name='delete-event'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
]