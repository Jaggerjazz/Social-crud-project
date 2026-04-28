from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Recipe, Profile
from .forms import RecipeForm

def home(request):
    return render(request, 'home.html', {})

def recipes(request):
    all_recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipes.html', {"recipes": all_recipes})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically logs you in after registering
            messages.success(request, "Account created successfully!")
            return redirect("home")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def search(request):
    query = request.GET.get('q')
    results = Recipe.objects.none()
    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        )
    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required
def profile(request):
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'recipes': user_recipes})

@login_required
def add_recipe(request):
    if request.method == "POST":
        # request.FILES is required for your recipe images!
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, "Recipe added successfully!")
            return redirect("recipes")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {"form": form})

@login_required
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_detail.html', {"recipe": recipe})

@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    # Security: only the author can edit
    if recipe.author != request.user:
        messages.error(request, "You don't have permission to edit this recipe.")
        return redirect('profile')

    if request.method == "POST":
        # request.FILES ensures the image stays or gets updated
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'edit_recipe.html', {"form": form, "recipe": recipe})

@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.author == request.user:
        recipe.delete()
        messages.success(request, "Recipe deleted successfully!")
    else:
        messages.error(request, "You don't have permission to delete this recipe.")
    return redirect('profile')