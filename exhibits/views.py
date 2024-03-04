from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MapExhibitContribution
from .forms import MapExhibitContributionForm
from django.views.generic import CreateView
# Create your views here.

def testing_map(request):
    return render(request, 'exhibits/Maps/syria_recipes_and_cultures.html') 

class MapExhibitContributionCreateView(LoginRequiredMixin, CreateView):
    model = MapExhibitContribution
    form_class = MapExhibitContributionForm
    template_name = 'exhibits/Contact/exhibits_contribute.html'
    success_url = reverse_lazy('testing_map')
    
    def form_valid(self, form):
        form.instance.username_id = self.request.user.id
        return super().form_valid(form)
    