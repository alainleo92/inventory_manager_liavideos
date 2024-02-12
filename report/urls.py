from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Export_Event

urlpatterns = [
    path('export/<int:event_id>', Export_Event.as_view(), name='export-pdf'),
]