from django.shortcuts import render, redirect
from .forms import ExampleForm


# Create your views here.
def index(request):
	a = request.GET
	print(a)
    # logic of view will be implemented here
	return render(request, "home.html")