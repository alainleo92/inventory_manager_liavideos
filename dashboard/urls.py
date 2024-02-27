from django.urls import path
from .views import Dashboard, Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dash'),   
]