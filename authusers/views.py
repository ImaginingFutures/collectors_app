from django.shortcuts import render, redirect
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import RegisterUserForm

import logging

logger = logging.getLogger("ifcollectors")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and password is not None:
            login(request, user)
            next_url = request.POST.get('next', 'home')
            messages.success(request, f"Hi again {username} :)")
            return redirect(next_url)
            
        else:
            
            messages.error(request, f"Invalid username \({username}\) or password.")
            return redirect('login')
        
    else:
        next_url = request.GET.get('next', 'home')
        return render(request, 'authusers/login.html', {'next': next_url})


def logout_user(request):
    logout(request)
    messages.success(request, "See you soon :)")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Associate recent user with the group.
            group, created = Group.objects.get_or_create(name='public_users')
            group.user_set.add(user)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(request, f"Welcome {username}")
                next_url = request.POST.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return render(request, 'authusers/register.html', {'form': form})
        else:
            # if form is not valid
            messages.error(request, "Please correct the errors below.")
            return render(request, 'authusers/register.html', {'form': form})
    else:
        form = RegisterUserForm()
        next_url = request.GET.get('next', 'home')
        return render(request, 'authusers/register.html', {'form': form, 'next': next_url})