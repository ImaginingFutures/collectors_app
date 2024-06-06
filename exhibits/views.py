from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from .models import MapExhibitContribution
from .forms import MapExhibitContributionForm
from django.views.generic import CreateView, DetailView
# Create your views here.

def testing_map(request):
    return render(request, 'exhibits/Maps/syria_recipes_and_cultures.html') 

def kakuma(request):
    return render(request, 'exhibits/Maps/kakuma.html') 

class MapExhibitContributionCreateView(CreateView):
    model = MapExhibitContribution
    form_class = MapExhibitContributionForm
    template_name = 'exhibits/Contact/exhibits_contribute.html'
    success_url = reverse_lazy('submissions')
    
    def form_valid(self, form):
        form.instance.username_id = self.request.user.id
        messages.success(self.request, f"Your contribution was successfully sent.")
        return super().form_valid(form)

class UserSubmissions(DetailView):
    model = User
    template_name= 'exhibits/Submissions/user_submissions.html'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            user_submissions = MapExhibitContribution.objects.filter(
                models.Q(
                    username = user
                )
            )
        else:
            user_submissions = MapExhibitContribution.objects.none()
        
        context['submissions'] = user_submissions
        return context
    
    