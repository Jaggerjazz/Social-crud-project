from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q  # For search logic
from .models import Recipe  #work with images

def home(request):
	return render(request, 'home.html',{})


def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Account created successfully")
			return redirect ("login")
		else:
			for error in form.errors.values():
                		messages.error(request, error)

	else:
		form = UserCreationForm()

	return render(request, "register.html", {"form":form})

def search(request):
    query = request.GET.get('q')
    results = Recipe.objects.none()
    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        )
    return render(request, 'search_results.html', {'results': results, 'query': query})

