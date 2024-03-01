from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView

urlpatterns = [
    path('user/signup/', SignUpView.as_view(), name='signup'),
    path('user/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('user/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]