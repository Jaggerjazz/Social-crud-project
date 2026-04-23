from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # Recipes
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_detail'),    path('recipes/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipes/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    
    # Login & Logout (Built-in Django)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    # Registration (The missing link!)
    path('register/', views.register, name='register'),

    #Profile
    path('profile/', views.profile, name='profile'),
]