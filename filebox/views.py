from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.models import User

from dal import autocomplete

import logging

logger = logging.getLogger("ifcollectors")

# Create your views here.
