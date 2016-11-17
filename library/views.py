from django.shortcuts import render, redirect
from stronghold.decorators import public
from authtools.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.contrib import messages

@public
def home(request):
	return render(request, "index.html")

	
@public
def contactus(request):
	return render(request, 'contact.html')

@public
def register_view(request):
    next = request.GET.get('next')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        if next:
            return redirect(next)
        return redirect(reverse('index'))

    context = {
        "form": form,
    }
    return render(request, "login.html", context)

@public
def update_profile(request):
	form = UserChangeForm(request.POST or None, instance=User.object.get(id=request.user.pk))
	if form.is_valid():
		user.save()
		return redirect(reverse('index'))
	context = {
		"form" : form,
	}
	return render(request, "form.html", context)