from django.shortcuts import render

# Create your views here.
def home(requerst):
	titulo = 'HOME'
	return render(request, 'home.html', {'titulo' : titulo})