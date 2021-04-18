from django.shortcuts import render

# Create your views here.

posts = [
	{
		'author': 'CoreyMS',
		'title': 'Blog Post 1',
		'content': 'First post!',
		'date': '1/1/21'
	},
	{
		'author': 'Jane Doe',
		'title': 'Blog Post 2',
		'content': '2e2',
		'date': 'fizzywig'
	}
]

def index(request):
	context = {
		'posts': posts
	}

	return render(request, 'index.html', context)
