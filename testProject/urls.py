from django.contrib import admin
from django.urls import path, include
from recipeApp import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipeApp.urls')), 
]