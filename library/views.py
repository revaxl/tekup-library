from django.shortcuts import render
from stronghold.decorators import public

@public
def home(request):
	return render(request, "index.html")

	
@public
def contactus(request):
	return render(request, 'contact.html')