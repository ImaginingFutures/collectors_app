from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.template.loader import render_to_string

from .token import token_generator


import logging

logger = logging.getLogger("ifcollectors")

class RegisterUserForm(UserCreationForm):
    
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2'
        )
        
    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'authusers/activate_account.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        