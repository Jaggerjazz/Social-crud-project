from django.contrib import admin
from .models import Profile, Category, Recipe

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Recipe)