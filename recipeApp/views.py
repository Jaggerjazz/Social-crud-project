from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
	return render(request, 'home.html',{})


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
    return render(request, 'profile.html', {'user': request.user})

@login_required
def my_recipes(request):
    # Your logic for user's recipes
    return render(request, 'my_recipes.html')

@login_required
def favorites(request):
    # Your logic for favorites
    return render(request, 'favorites.html')

