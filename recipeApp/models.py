from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    
    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
        ('appetizer', 'Appetizer'),
        ('snack', 'Snack'),
        ('vegetarian', 'Vegetarian'),
        ('quick', 'Quick & Easy'),
    ]
    
    categories = models.ManyToManyField(Category, related_name='recipes', blank=True)
    prep_time = models.IntegerField(help_text="Preparation time in minutes", blank=True, null=True)
    cook_time = models.IntegerField(help_text="Cooking time in minutes", blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        if self.prep_time and self.cook_time:
            return self.prep_time + self.cook_time
        return None
    
    def is_favorited_by(self, user):
        """Check if recipe is favorited by a user"""
        if user.is_authenticated:
            return self.favorited_by.filter(id=user.id).exists()
        return False
