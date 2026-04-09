from django.contrib import admin
from django.urls import path, include
from recipeApp import views  # <--- THIS IS THE IMPORTANT LINE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipeApp.urls')), # <--- This connects to the file you just showed me
]