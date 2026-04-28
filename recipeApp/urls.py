from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home and Register
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    # Search Functionality
    path('search/', views.search, name='search'),

    # Authentication (Login/Logout)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # Updated Logout: Simple and compatible with POST requests
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]