from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone  
from datetime import timedelta  
from django.contrib.auth.models import User  
from django.http import JsonResponse
from .models import Recipe, Profile, Category
from .forms import RecipeForm

def home(request):
    featured_recipes = Recipe.objects.all().order_by('-created_at')[:6]
    total_recipes = Recipe.objects.count()
    total_users = User.objects.count()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_recipes_count = Recipe.objects.filter(created_at__gte=thirty_days_ago).count()
    
    category_counts = {}
    for category in Category.objects.all():
        count = category.recipes.count()
        if count > 0:
            category_counts[category.name] = count
    
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = request.user.favorite_recipes.values_list('id', flat=True)
    
    context = {
        'featured_recipes': featured_recipes,
        'total_recipes': total_recipes,
        'total_users': total_users,
        'recent_count': recent_recipes_count,
        'categories_count': category_counts,
        'user_favorites': user_favorite_ids,
    }
    return render(request, 'home.html', context)

def recipes(request):
    category_filter = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', '-created_at')
    
    all_recipes = Recipe.objects.all()
    
    if category_filter and category_filter != 'all':
        if 'quick' in category_filter.lower():
            all_recipes = all_recipes.filter(
                Q(category__name__icontains='Quick'),
                prep_time__lte=30
            ).extra(
                where=["(prep_time + cook_time) <= 30"]
            )
        else:
            all_recipes = all_recipes.filter(category__name__iexact=category_filter)
    
    if sort_by == 'title':
        all_recipes = all_recipes.order_by('title')
    elif sort_by == '-title':
        all_recipes = all_recipes.order_by('-title')
    elif sort_by == 'created_at':
        all_recipes = all_recipes.order_by('created_at')
    elif sort_by == '-created_at':
        all_recipes = all_recipes.order_by('-created_at')
    elif sort_by == 'prep_time':
        all_recipes = all_recipes.order_by('prep_time')
    elif sort_by == '-prep_time':
        all_recipes = all_recipes.order_by('-prep_time')
    else:
        all_recipes = all_recipes.order_by('-created_at')
    
    categories = Category.objects.all()
    
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = request.user.favorite_recipes.values_list('id', flat=True)
    
    context = {
        'recipes': all_recipes,
        'current_category': category_filter,
        'current_sort': sort_by,
        'categories': categories,
        'favorite_ids': list(favorite_ids),
    }
    
    return render(request, 'recipes.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    is_favorited = False
    
    if request.user.is_authenticated:
        is_favorited = recipe.favorited_by.filter(id=request.user.id).exists()
    
    context = {
        "recipe": recipe,
        "is_favorited": is_favorited,
        "favorite_count": recipe.favorited_by.count(),
    }
    
    return render(request, 'recipe_detail.html', context)

def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    recipe_results = Recipe.objects.none()
    user_results = User.objects.none()
    
    if query:
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(ingredients__icontains=query) |
            Q(instructions__icontains=query)
        )
        user_results = User.objects.filter(username__icontains=query)
    elif category:
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=category) | 
            Q(ingredients__icontains=category)
        )
    
    context = {
        'recipe_results': recipe_results,
        'user_results': user_results,
        'query': query or category
    }
    
    return render(request, 'search_results.html', context)

def user_profile(request, username):
    target_user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=target_user).order_by('-created_at')
    return render(request, 'user_profile.html', {
        'target_user': target_user,
        'recipes': recipes
    })

@login_required
def profile(request):
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'recipes': user_recipes})

@login_required
def add_recipe(request):
    if request.method == "POST":
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
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if recipe.author != request.user:
        messages.error(request, "You don't have permission to edit this recipe.")
        return redirect('profile')

    if request.method == "POST":
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

@login_required
def favorite_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    
    if recipe.favorited_by.filter(id=request.user.id).exists():
        recipe.favorited_by.remove(request.user)
        messages.success(request, f'Removed "{recipe.title}" from favorites.')
    else:
        recipe.favorited_by.add(request.user)
        messages.success(request, f'Added "{recipe.title}" to favorites!')
    
    return redirect(request.META.get('HTTP_REFERER', 'recipes'))

@login_required
def favorites_page(request):
    favorite_recipes = request.user.favorite_recipes.all().order_by('-created_at')
    
    context = {
        'favorite_recipes': favorite_recipes,
        'total_favorites': favorite_recipes.count(),
    }
    
    return render(request, 'favorites.html', context)

@login_required
def ajax_favorite_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    
    if recipe.favorited_by.filter(id=request.user.id).exists():
        recipe.favorited_by.remove(request.user)
        is_favorited = False
        message = 'Removed from favorites'
    else:
        recipe.favorited_by.add(request.user)
        is_favorited = True
        message = 'Added to favorites'
    
    return JsonResponse({
        'is_favorited': is_favorited,
        'message': message,
        'favorite_count': recipe.favorited_by.count()
    })