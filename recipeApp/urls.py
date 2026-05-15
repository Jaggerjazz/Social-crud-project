from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('favorite/<int:id>/', views.favorite_recipe, name='favorite_recipe'),
    path('ajax/favorite/<int:id>/', views.ajax_favorite_recipe, name='ajax_favorite_recipe'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]