from django.db import models
from django.contrib.auth.models import User

# --- MELANIE'S CODE ---
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     bio = models.TextField(blank= True)
#     student_id = models.IntegerField(blank = True)
#     enrolled = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.user.username

# 

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title