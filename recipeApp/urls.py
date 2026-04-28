from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home and Register
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    # Search Functionality
    path('search/', views.search, name='search'),

    # Recipes (Melanie's CRUD features)
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Authentication (Keep your updated POST-compatible versions)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]