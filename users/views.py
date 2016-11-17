from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from stronghold.decorators import public
from django.views.generic.edit import  UpdateView
from django.core.urlresolvers import reverse
from django.contrib import messages
"""local project import"""
from .forms import updateProfile


@public
def profile(request, id=None):
    return render(request, 'profile.html')


def update(request, id=None):
    form = updateProfile(request.POST or None, instance = request.user)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        user = form.save(commit=False)
        user.name = name
        user.save()
        return redirect(reverse('index'))
    context = {
        "form" : form,
    }
    return render(request, 'form.html', context)




@public
def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    form2 = VisitorForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        messages.info(request, 'Add your CIN using the update button!')
        if next:
            return redirect(next)
        return redirect(reverse('users:profile', kwargs={'id':request.user.pk}))

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)

