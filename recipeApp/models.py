from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	bio = models.TextField(blank= True)

	def __str__(self):
		return self.user.username
	
class Recipe(models.Model):
	title = models.CharField(max_length=100)
	ingredients = models.TextField()
	instructions = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	
	