from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
	return render(request, 'home.html',{})

def recipes(request):
	return render(request, 'recipes.html',{})
def add_recipe(request):
	return render(request, 'add_recipe.html',{})

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
	return render(request, 'profile.html', {})

@login_required
def add_recipe(request):
	return render(request, 'add_recipe.html', {})

@login_required
def logout(request):
	return render(request, 'logout.html', {})

