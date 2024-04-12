from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .token import token_generator
from .forms import RegisterUserForm

user_model = get_user_model()

import logging

logger = logging.getLogger("ifcollectors")

class SignUpView(CreateView):
    form_class = RegisterUserForm 
    template_name = 'authusers/register.html'
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        
        user = form.save()
        user.is_active = False # Turns the user status to inactive
        user.save()

        form.send_activation_email(self.request, user)

        return to_return

class ActivateView(RedirectView):

    url = reverse_lazy('success')

    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'authusers/activate_account_invalid.html')


class CheckEmailView(TemplateView):
    template_name = 'authusers/check_email.html'

class SuccessView(TemplateView):
    template_name = 'authusers/success.html'

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
            return redirect('login_user')
        
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