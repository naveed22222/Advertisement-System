from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .middlewares import guest
from .forms import *


# Create your views here.
@guest
def LoginView(request):
    template_name = "Login.html"

    if request.method == 'POST':

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Dashboard')
        else:
            messages.success(request, "Invalid Credential.")
            return redirect('Login')
    else:
        return render(request, template_name)


@login_required(login_url='Login')
def LogoutView(request):
    logout(request)
    return redirect('Login')


@guest
def RegisterUser(request):
    template_name = 'RegisterUser.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('Login')
    else:
        initial_data = {'username': '', 'password1': '', 'password2': '', 'first_name': '', 'last_name': '', 'email': ''}
        form = RegisterForm(initial=initial_data)

    param = {
        'form': form
    }
    return render(request, template_name, param)




