from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recipe, Profile
from .forms import RecipeForm

def home(request):
	return render(request, 'home.html',{})

def recipes(request):
	all_recipes = Recipe.objects.all().order_by('-created_at')
	return render(request, 'recipes.html', {"recipes": all_recipes})

def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Account created successfully")
			return redirect ("login")
	else:
		form = UserCreationForm()

	return render(request, "register.html", {"form":form})

@login_required
def profile(request):
	user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
	return render(request, 'profile.html', {})

@login_required
def logout(request):
	return render(request, 'logout.html', {})

@login_required
def add_recipe(request):
	if request.method == "POST":
		form = RecipeForm(request.POST)
		if form.is_valid():
			recipe = form.save(commit=False)
			recipe.author = request.user
			recipe.save()
			messages.success(request, "Recipe added successfully")
			return redirect("recipes")
		else:
			messages.error(request, "Please correct the errors below.")
	else:
		form = RecipeForm()

	return render(request, 'add_recipe.html', {"form": form})

@login_required
def recipe_detail(request, id):
	recipe = Recipe.objects.get(id=id)
	return render(request, 'recipe_detail.html', {"recipe": recipe})

@login_required
def delete_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    # Make sure only the author can delete
    if recipe.author == request.user:
        recipe.delete()
        messages.success(request, "Recipe deleted successfully!")
    else:
        messages.error(request, "You don't have permission to delete this recipe.")
    return redirect('profile')

@login_required
def edit_recipe(request, id):
	recipe = Recipe.objects.get(id=id)
	# Make sure only the author can edit
	if recipe.author != request.user:
		messages.error(request, "You don't have permission to edit this recipe.")
		return redirect('profile')

	if request.method == "POST":
		form = RecipeForm(request.POST, instance=recipe)
		if form.is_valid():
			form.save()
			messages.success(request, "Recipe updated successfully!")
			return redirect('recipe_detail', id=recipe.id)
		else:
			messages.error(request, "Please correct the errors below.")
	else:
		form = RecipeForm(instance=recipe)

	return render(request, 'edit_recipe.html', {"form": form, "recipe": recipe})


