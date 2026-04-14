from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),

    # Login & Logout (Built-in Django)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html'), name='logout'),
    
    # Registration (The missing link!)
    path('register/', views.register, name='register'),
    
    path('profile/', views.profile, name='profile'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('favorites/', views.favorites, name='favorites'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('edit-recipe/', views.edit_recipe, name='edit_recipe'),
]