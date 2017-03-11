from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user


from .forms import RegistrationForm, LoginForm


def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('users:login')
    return render(request, 'users/register_form.html', {'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            login_user(request, user)
            return redirect('shop:product_list')
    return render(request, 'users/login_form.html', {'form': form})


def logout(request):
    logout_user(request)
    return redirect('login')
